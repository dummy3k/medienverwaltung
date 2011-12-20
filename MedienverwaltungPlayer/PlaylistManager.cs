using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization.Formatters.Binary;
using System.Text;

namespace MedienverwaltungPlayer
{
    [Serializable]
    public class PlaylistManager
    {
        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);
 
        public VlcPlayer _vlcPlayer = new VlcPlayer();

        public static VlcPlayer vlcPlayer = null;

        public List<Playlist> playlists { get; private set; }
        public Playlist currentPlaylist { get; set; }

        public String rootFolder { get; set; }
        
        private PlaylistManager()
        {
            this.playlists = new List<Playlist>();
            PlaylistManager.vlcPlayer = _vlcPlayer;
            
            
        }

        private static PlaylistManager instance = null;
        public static PlaylistManager getInstance()
        {
            if (instance == null)
            {
                log.Info("creating PlaylistMangager Instance");
                instance = new PlaylistManager();
                vlcPlayer.playlistManager = instance;
            }
            return instance;
        }             

        public String currentlyPlayedFile()
        {
            if (currentPlaylist != null)
            {
                return currentPlaylist.currentlyPlayedFile();
            }

            return null;
        }

        public Playlist findPlaylistById(Int32 id)
        {
            foreach (var playlist in playlists)
            {
                if (playlist.id == id)
                {
                    return playlist;
                }
            }

            return null;
        }

        public void select(Playlist playlist=null)
        {
            if (playlist == null && currentPlaylist == null)
            {
                currentPlaylist = playlists.FirstOrDefault();
            }

            if (playlist != null)
            {
                currentPlaylist = playlist;
            }
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
                currentPlaylist.update();
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

        public void deleteCurrentPlaylist()
        {
            if (this.currentPlaylist != null)
            {
                this.playlists.Remove(this.currentPlaylist);
                this.currentPlaylist = null;
                select();
            }
        }
    }
}
