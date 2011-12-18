using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MedienverwaltungPlayer
{
    class PlaylistEntry 
    {
        public String filename { get; private set; }
        public Int32 time { get; set; }

        public void play()
        {
            PlaylistManager.vlcPlayer.start(filename);
        }

        public void stop()
        {
            PlaylistManager.vlcPlayer.stop();
        }
    }
}
