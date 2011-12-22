using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Diagnostics;
using System.Web;
using System.IO;
using System.Windows.Forms;

namespace MedienverwaltungPlayer
{
    [Serializable]
    public class VlcPlayer
    {
        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);

        public static MainForm mainForm = null;

        public String baseUrl { get; set; }
        public Int32 time { get; set; }
        public Int32 length { get; private set; }
        public String state { get; private set; }
        public String currentPath { get; set; }


        private Boolean _playing = false;
        public Boolean playing
        {
            get
            {
                return _playing;
            }

            private set
            {
                if (_playing != value)
                {
                    _playing = value;
                    if (mainForm != null)
                    {
                        mainForm.onPlayingChange(value);
                    }
                }
            }
        }
        public static Process vlcProcess { get; set; }
        public String vlcLocation { get; set; }
        public PlaylistManager playlistManager { get; set; }

        public VlcPlayer(String baseUrl = "http://localhost:8080/")
        {
            log.Info("creating VlcPlayer with baseUrl= '" + baseUrl + "'");

            this.baseUrl = baseUrl;
            this.vlcLocation = @"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe";
            resetStatus();
        }

        public void resetStatus()
        {
            this.time = 0;
            this.state = null;
            this.currentPath = null;
            this.playing = false;
        }
        
        public void destory() {
            if (vlcProcess != null && vlcProcess.HasExited == false)
            {
                vlcProcess.Kill();
            }
        }

        private Boolean _togglePause()
        {
            if (callUrl(baseUrl + "requests/status.xml?command=pl_pause&id=4") != null)
            {
                if (this.state == "stop" || state == "paused")
                {
                    playing = true;
                }
                else
                {
                    playing = false;
                }

                return true;
            }
            else
            {
                return false;
            }
        }

        public Boolean togglePause(String filenameAbsolute = null)
        {
            if (readStatus())
            {
                if (filenameAbsolute != null)
                {
                    String filename = new System.IO.FileInfo(filenameAbsolute).Name;

                    if (this.currentPath == filenameAbsolute)
                    {
                        return _togglePause();
                    }
                    else
                    {
                        return start(filenameAbsolute);
                    }
                }
                else
                {
                    return _togglePause();
                }
            }
            else
            {
                return start(filenameAbsolute);
            }
        }

        private Boolean start(String filenameAbsolute, Int32 time=0)
        {
            if (File.Exists(vlcLocation) == false)
            {
                log.Error("did not find vlc application");
                return false;
            }

            String paramList = "--control=http --one-instance";
            String filename  = new FileInfo(filenameAbsolute).Name;

            log.Info("starting '" + filenameAbsolute + "' with time=" + time);

            Process newProcess = Process.Start(vlcLocation, paramList + " \"" + filenameAbsolute + "\"");

            if (VlcPlayer.vlcProcess == null || VlcPlayer.vlcProcess.HasExited)
            {
                VlcPlayer.vlcProcess = newProcess;
            }
            
            if(time != 0) {
                const int SLEEP_TIME = 250;
                const int MAX_WAIT = 2500;

                for(int i=0; i*SLEEP_TIME<MAX_WAIT; i++) {
                    System.Threading.Thread.Sleep(SLEEP_TIME);

                    if (readStatus() && this.length > 0 && this.currentPath == filenameAbsolute)
                    {
                        if (seek(time))
                        {
                            log.Info("successfully seeked to " + time + " seconds after waiting " + (i * SLEEP_TIME) + " ms");
                            return true;
                        }
                        else
                        {
                            log.Debug("seek failed");
                        }
                    }
                    else
                    {
                        log.Debug("readStatus failed()");
                    }
                }
            }

            return false;
        }

        public Boolean play(String filenameAbsolute=null, Int32 time=0)
        {
            if (readStatus())
            {
                if (filenameAbsolute != null)
                {
                    if (this.currentPath == filenameAbsolute)
                    {
                        if (state == "stop" || state == "paused")
                        {
                            log.Debug("play(): toggling pause because video is in state " + state);
                            return _togglePause();
                        }
                        else
                        {
                            log.Debug("play(): already playing ...");
                            return true;
                        }

                    }
                    else
                    {
                        log.Debug("play(): starting new vlc because current path '" + (this.currentPath != null && this.currentPath != "" ? new FileInfo(this.currentPath).Name : "(empty)") + "' is different from our '" + new FileInfo(filenameAbsolute).Name + "'");
                        return start(filenameAbsolute, time);
                    }
                }
                else
                {
                    if (state == "stop" || state == "paused")
                    {
                        log.Debug("play(): toggling pause because video is in state " + state);
                        return _togglePause();
                    }
                    else
                    {
                        log.Debug("play(): already playing ...");
                        return true;
                    }
                }
            } else {
                log.Debug("play(): starting new vlc because no running instance was found");
                return start(filenameAbsolute, time);
            }
        }

        public Boolean stop()
        {
            if (readStatus())
            {
                if (callUrl(baseUrl + "requests/status.xml?command=pl_stop") != null)
                {
                    playing = false;
                    return true;
                }

                else
                {
                    return false;
                }
            }
            else
            {
                return false;
            }                
        }

        public Boolean seek(Int32 time)
        {
            var result = callUrl(baseUrl + "requests/status.xml?command=seek&val=" + time);
            //log.Info("seek result: " + result);
            return result != null;
        }

        public Process findRunningVlcProcess()
        {
            // find current vlc process
            foreach (var process in Process.GetProcessesByName("vlc"))
            {
                if (process.HasExited == false)
                {
                    return process;
                }
            }

            return null;
        }

        public Boolean readStatus()
        {
            if (VlcPlayer.vlcProcess != null)
            {
                VlcPlayer.vlcProcess.Refresh();

                if (VlcPlayer.vlcProcess.HasExited)
                {
                    VlcPlayer.vlcProcess = findRunningVlcProcess();
                }
            }
            else
            {
                VlcPlayer.vlcProcess = findRunningVlcProcess();
            }

            if (VlcPlayer.vlcProcess == null)
            {
                return false;
            }

            var statusXml = callUrl(baseUrl + "requests/status.xml");

            if (statusXml == null)
            {
                return false;
            }

            XmlDocument doc = new XmlDocument();
            doc.LoadXml(statusXml);

            this.time = Int32.Parse(doc.DocumentElement.SelectSingleNode("/root/time").InnerText);
            this.length = Int32.Parse(doc.DocumentElement.SelectSingleNode("/root/length").InnerText);
            this.state = doc.DocumentElement.SelectSingleNode("/root/state").InnerText;

            var tag = doc.DocumentElement.SelectSingleNode("/root/information/meta-information/title").FirstChild;
            var element = (XmlCDataSection)tag;

            var data = element.Data;

            this.playing = this.state == "playing";

            var status = "time: " + time + "/" + length + ". state: " + state + " @ '" + (currentPath != null && currentPath != "" ? new FileInfo(currentPath).Name : "(leer)") + "'";
            log.Info(status);
            
            var playlistXml = callUrl(baseUrl + "requests/playlist.xml");

            if (playlistXml != null)
            {
                doc = new XmlDocument();
                doc.LoadXml(playlistXml);

                var leaf = doc.DocumentElement.SelectSingleNode("//leaf[@current='current']");
                if (leaf != null)
                {
                    var val = leaf.Attributes.GetNamedItem("uri").Value;
                    this.currentPath = HttpUtility.UrlDecode(val.Replace("file:///", "").Replace("file://", "").Replace("/", "\\"));
                }
            }

            return true;
        }

        private String callUrl(String url)
        {
            log.Info("http get '" + url + "'");
            System.Net.WebRequest req = System.Net.WebRequest.Create(url);

            req.ContentType = "text/xml";
            req.Method = "GET";

            try
            {
                System.Net.WebResponse resp = req.GetResponse();
                if (resp == null) return null;
                System.IO.StreamReader sr = new System.IO.StreamReader(resp.GetResponseStream());

                var responsecontent = sr.ReadToEnd().Trim();
                return responsecontent;
            }
            catch (Exception e)
            {
                log.Error("error calling url '" + url + "':", e);
                return null;
            }
        }

    }
}