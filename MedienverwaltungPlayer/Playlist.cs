using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MedienverwaltungPlayer
{
    class Playlist
    {
        private List<PlaylistEntry> playlistEntries = new List<PlaylistEntry>();

        private PlaylistEntry currentPlaylistEntry = null;

        public void play()
        {
            if (currentPlaylistEntry != null)
            {
                currentPlaylistEntry.play();
            }
            else
            {
                currentPlaylistEntry = playlistEntries.First();

                if (currentPlaylistEntry != null)
                {
                    currentPlaylistEntry.play();
                }
            }
        }

        public void stop() {
            if (currentPlaylistEntry != null)
            {
                currentPlaylistEntry.stop();
            }
        }

        public void next()
        {
            stop();

            Boolean useNext = true;

            foreach(var entry in playlistEntries) {
                
            }
        }

    }
}
