using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Threading;
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
        public Boolean fileNotFound { get; set; }

        public Boolean check()
        {
            fileNotFound = File.Exists(path) == false;
            return !fileNotFound;
        }

        public Playlist parent { get; private set; }
        
        public PlaylistEntry(String path, Playlist parent)
        {
            this.parent = parent;
            this.path = path;
            this.time = 0;
            this.watched = false;
            this.fileNotFound = false;
        }

        public void play()
        {
            PlaylistManager.vlcPlayer.play(path, this.time);
        }

        public void stop()
        {
            update();
            PlaylistManager.vlcPlayer.stop();
        }

        public void update()
        {
            if (PlaylistManager.vlcPlayer.readStatus())
            {
                if (PlaylistManager.vlcPlayer.currentFilename == filename)
                {
                    if (PlaylistManager.vlcPlayer.time != 0)
                    {
                        log.Info("update(): setting saved time to " + PlaylistManager.vlcPlayer.time);
                        this.time = PlaylistManager.vlcPlayer.time;
                    }

                    if (PlaylistManager.vlcPlayer.length != 0)
                    {
                        this.length = PlaylistManager.vlcPlayer.length;
                    }
                }

                if (PlaylistManager.vlcPlayer.time == 0
                    && PlaylistManager.vlcPlayer.length == 0
                    && PlaylistManager.vlcPlayer.state == "stop"
                    && this.time > 5 && this.length > 5
                    && this.time > this.length - 30 )
                {
                    log.Info("setting watched to true and watching next video()");
                    this.watched = true;
                    this.time = 0;
                    parent.next();
                }
            }
            else
            {

            }
        }

        public void pause()
        {
            if (PlaylistManager.vlcPlayer.readStatus())
            {
                update();
                PlaylistManager.vlcPlayer.togglePause();
            }
            else
            {
                play();
            }
        }
    }
}
