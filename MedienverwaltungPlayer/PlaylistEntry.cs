using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading;
using System.Threading.Tasks;
using log4net;

namespace MedienverwaltungPlayer
{
    [Serializable]
    public class PlaylistEntry
    {
        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);
 
        public String path { get; private set; }
        public String filename
        {
            get
            {
                return new FileInfo(path).Name;
            }
        }

        public Int32 time { get; set; }
        public Int32 length { get; set; }
        public Boolean watched { get; set; }

        public Playlist parent { get; private set; }
        
        public PlaylistEntry(String path, Playlist parent)
        {
            this.parent = parent;
            this.path = path;
            this.time = 0;
            this.watched = false;
        }

        public void play()
        {
            var time = this.time;
            log.Info("playing " + path);
            PlaylistManager.vlcPlayer.start(path);
            log.Info("seeking to " + time);
            PlaylistManager.vlcPlayer.seek(time);
        }

        public void stop()
        {
            update();
            PlaylistManager.vlcPlayer.stop();
        }

        public void update()
        {
            PlaylistManager.vlcPlayer.readStatus();

            if (PlaylistManager.vlcPlayer.time != 0)
            {
                log.Info("update(): setting saved time to " + PlaylistManager.vlcPlayer.time);
                this.time = PlaylistManager.vlcPlayer.time;
                this.length = PlaylistManager.vlcPlayer.length;
            }
            /*
            log.Debug("this.watched = " + this.watched);
            log.Debug("this.time = " + this.time);
            log.Debug("PlaylistManager.vlcPlayer.length = " + PlaylistManager.vlcPlayer.length);
            log.Debug("PlaylistManager.vlcPlayer.state = " + PlaylistManager.vlcPlayer.state);
            */
            if (this.watched == false && PlaylistManager.vlcPlayer.time == 0 && PlaylistManager.vlcPlayer.length == 0 && PlaylistManager.vlcPlayer.state == "stop")
            {
                log.Info("setting watched to true and watching next video()");
                this.watched = true;
                parent.next();
            }
        }

        public void pause()
        {
            if (PlaylistManager.vlcPlayer.started)
            {
                if (PlaylistManager.vlcPlayer.playing)
                {
                    update();
                }
                PlaylistManager.vlcPlayer.togglePause();
            }
            else
            {
                play();
            }
        }
    }
}
