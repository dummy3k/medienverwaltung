using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MedienverwaltungPlayer
{
    class PlaylistManager
    {
        public List<Playlist> playlists { get; private set; }

        public static VlcPlayer vlcPlayer = new VlcPlayer();

        private Playlist _currentPlaylist = null;

        public Playlist currentPlaylist
        {
            get 
            { 
                return _currentPlaylist; 
            }

            set 
            {
                if (_currentPlaylist != null)
                {
                    _currentPlaylist.stop();
                }
                _currentPlaylist = value;
            }
        }

        public static PlaylistManager load(String path)
        {
            PlaylistManager playlistManager = null;
            System.Xml.Serialization.XmlSerializer x = new System.Xml.Serialization.XmlSerializer(typeof(PlaylistManager));
            using (var file = System.IO.File.Open(path, System.IO.FileMode.Open))
            {
                playlistManager = (PlaylistManager)x.Deserialize(file);
            }

            return playlistManager;
        }

        public void save(String path)
        {
            System.Xml.Serialization.XmlSerializer x = new System.Xml.Serialization.XmlSerializer(this.GetType());
            using (var file = System.IO.File.Open(path, System.IO.FileMode.CreateNew))
            {
                x.Serialize(file, this);
            }
        }
    }
}
