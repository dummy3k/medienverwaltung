using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;
using System.Threading.Tasks;

namespace MedienverwaltungPlayer
{
    [Serializable]
    public class PlaylistManager
    {
        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);
 
        public static VlcPlayer vlcPlayer = new VlcPlayer();
        public List<Playlist> playlists { get; private set; }
        public Playlist currentPlaylist { get; set; }
        private Boolean tryNextTick = false;

        public String rootFolder { get; set; }
        
        public PlaylistManager()
        {
            this.playlists = new List<Playlist>();
        }

        public String currentlyPlayedFile()
        {
            if (currentPlaylist != null)
            {
                return currentPlaylist.currentlyPlayedFile();
            }

            return null;
        }

        public Playlist findByName(String name)
        {
            foreach (var playlist in playlists)
            {
                if (playlist.name == name)
                {
                    return playlist;
                }
            }

            return null;
        }

        public void play(Playlist playlist)
        {
            if (currentPlaylist != null)
            {
                currentPlaylist.play();
            }
            currentPlaylist = playlist;
        }

        public void play()
        {
            if (currentPlaylist != null)
            {
                play(currentPlaylist);
            }

            else
            {
                currentPlaylist = playlists.FirstOrDefault();
                
                if (currentPlaylist != null)
                {
                    play(currentPlaylist);
                }
            }
        }

        public void stop()
        {

            if (currentPlaylist != null)
            {
                tryNextTick = false;
                currentPlaylist.stop();
            }
        }

        public void pause()
        {
            if (currentPlaylist != null)
            {
                currentPlaylist.pause();
            }
            else
            {
                currentPlaylist = playlists.FirstOrDefault();

                if (currentPlaylist != null)
                {
                    currentPlaylist.pause();
                }
            }
        }

        public void update()
        {
            if (currentPlaylist != null)
            {
                if (vlcPlayer.playing)
                {
                    log.Info("updating!");
                    currentPlaylist.update();
                    tryNextTick = true;
                }
                else
                {
                    if (tryNextTick)
                    {
                        log.Info("updating once more!");
                        currentPlaylist.update();

                        tryNextTick = false;
                    }
                    else
                    {
                        log.Info("NOT updating because vlcPlayer.playing = " + vlcPlayer.playing);
                    }
    
                }
                              
            }
        }

        public void next()
        {
            if (currentPlaylist != null)
            {
                currentPlaylist.next();
            }
            else
            {
                log.Warn("no currentPlaylist!");
            }
        }

        public void prev()
        {
            if (currentPlaylist != null)
            {
                currentPlaylist.prev();
            }
        }

        public static PlaylistManager load(String path)
        {
            log.Info("loading from '" + path + "'");
            PlaylistManager playlistManager = null;

            BinaryFormatter binaryFormatter = new BinaryFormatter();
            using (var file = System.IO.File.Open(path, System.IO.FileMode.Open))
            {
                playlistManager = (PlaylistManager) binaryFormatter.Deserialize(file);
            }

            return playlistManager;
        }

        public void save(String path)
        {
            log.Info("saving to '" + path + "'");
            BinaryFormatter binaryFormatter = new BinaryFormatter();
            //System.Xml.Serialization.XmlSerializer x = new System.Xml.Serialization.XmlSerializer(typeof(PlaylistManager));
            using (var file = System.IO.File.Open(path, System.IO.FileMode.Create))
            {
                binaryFormatter.Serialize(file, this);
            }
        }
    }
}
