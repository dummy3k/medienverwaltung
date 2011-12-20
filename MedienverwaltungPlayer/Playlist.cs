using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Linq;
using System.Collections;


namespace MedienverwaltungPlayer
{
    [Serializable]
    public class Playlist
    {
        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);
 
        public String rootPath { get; private set; }
        public String name { get; set; }
        public List<PlaylistEntry> playlistEntries { get; set; }
        public PlaylistEntry currentPlaylistEntry { get; set; }
        public Int32 id = 0;


        public override String ToString()
        {
            return name;
        }

        public Playlist(String rootPath, String name)
        {
            this.rootPath = rootPath;
            this.name = name;
            this.currentPlaylistEntry = null;
            this.playlistEntries = new List<PlaylistEntry>();

            scanDirectory(rootPath);

            this.playlistEntries = (from x in playlistEntries
                                         orderby x.path ascending
                                         select x).ToList();
        }

        public String currentlyPlayedFile()
        {
            if (currentPlaylistEntry != null)
            {
                return currentPlaylistEntry.path;
            }

            return null;
        }

        public void scanDirectory(String path, int lvl = 0)
        {
            if (path == "")
            {

                return;
            }


            string[] files = Directory.GetFiles(path);

            SortedList all = new SortedList();

            foreach (var dirname in Directory.GetDirectories(path))
            {
                scanDirectory(Path.Combine(path, dirname), lvl + 1);
            }

            foreach (var filename in Directory.GetFiles(path))
            {
                log.Debug("adding file '" + filename + "' to playlist '" + name + "'");
                PlaylistEntry entry = new PlaylistEntry(Path.Combine(path, filename), this);
                playlistEntries.Add(entry);
            }
        }

        public void deleteEntry(PlaylistEntry entry)
        {
            if (entry == currentPlaylistEntry)
            {
                currentPlaylistEntry.stop();
            }

            playlistEntries.Remove(entry);
        }

        public void check()
        {
            var updatedEntries = new Playlist(rootPath, name);

            foreach (var entry in updatedEntries.playlistEntries)
            {
                
            }


            foreach (var entry in playlistEntries)
            {
                entry.check();
            }
        }

        public void play()
        {
            if (currentPlaylistEntry != null)
            {
                log.Info("play(): using current playlistEntry: " + currentPlaylistEntry.path);
                currentPlaylistEntry.play();
            }
            else
            {
                log.Info("play(): using next");
                next();
            }
        }

        public void play(PlaylistEntry entry)
        {
            if (currentPlaylistEntry != null)
            {
                currentPlaylistEntry.update();
            }
            currentPlaylistEntry = entry;
            play();
        }

        public void stop()
        {
            if (currentPlaylistEntry != null)
            {
                currentPlaylistEntry.stop();
            }
        }

        public void pause()
        {
            if (currentPlaylistEntry != null)
            {
                currentPlaylistEntry.pause();
            }
            else
            {
                next();
            }
        }

        public void update()
        {
            if (currentPlaylistEntry != null)
            {
                currentPlaylistEntry.update();
            }
            else
            {
                if (PlaylistManager.vlcPlayer.readStatus())
                {
                    foreach (var entry in playlistEntries)
                    {
                        if (entry.filename == PlaylistManager.vlcPlayer.currentFilename)
                        {
                            currentPlaylistEntry = entry;
                            currentPlaylistEntry.update();
                            return;
                        }
                    }
                }
            }
        }

        public void next()
        {
            stop();

            Boolean useNext = false;

            foreach (var entry in playlistEntries)
            {
                if (entry.watched == false && (useNext || currentPlaylistEntry == null))
                {
                    log.Info("next() found '" + entry.path + "' with watched = " + entry.watched + " @ " + entry.time);
                    currentPlaylistEntry = entry;
                    play();
                    return;
                }

                if (currentPlaylistEntry != null && entry.path == currentPlaylistEntry.path)
                {
                    useNext = true;
                }
            }

            log.Info("next() found nothing!");
        }

        public void prev()
        {
            stop();

            Boolean useNext = false;

            foreach (var entry in (from x in playlistEntries
                                    orderby x.path descending
                                    select x))
            {
                if (entry.watched == false && (useNext || currentPlaylistEntry == null))
                {
                    log.Info("prev() found '" + entry.path + "' with watched = " + entry.watched + " @ " + entry.time);
                    currentPlaylistEntry = entry;
                    play();
                    return;
                }

                if (currentPlaylistEntry != null && entry.path == currentPlaylistEntry.path)
                {
                    useNext = true;
                }
            }
            log.Info("prev() found nothing!");
        }
    }
}
