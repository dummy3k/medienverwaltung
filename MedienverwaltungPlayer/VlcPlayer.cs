using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Diagnostics;

namespace MedienverwaltungPlayer
{
    public class VlcPlayer
    {
        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);

        public String baseUrl { get; set; }
        public Int32 time { get; set; }
        public Int32 length { get; private set; }
        public String state { get; private set; }
        public String currentFilename { get; set; }


        public Boolean playing { get; private set; }
        public Boolean started { get; private set; }


        public VlcPlayer(String baseUrl = "http://localhost:8080/")
        {
            log.Info("creating VlcPlayer with baseUrl= '" + baseUrl + "'");
            this.baseUrl = baseUrl;
            this.playing = false;
            this.started = false;
        }

        public String togglePause()
        {
            callUrl(baseUrl + "requests/status.xml?command=pl_pause");
            System.Threading.Thread.Sleep(300);
            readStatus();


            return "done";
        }

        public String start(String filenameAbsolute)
        {
            String vlcExe = @"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe";

            String filename = new System.IO.FileInfo(filenameAbsolute).Name;

            readStatus();
            stop();

            if (currentFilename == filename)
            {
                play();
                return "already running";
            }
            String paramList = "--control=http --one-instance";

            Process.Start(vlcExe, paramList + " \"" + filenameAbsolute + "\"");
            System.Threading.Thread.Sleep(2000);

            readStatus();

            return "done";
        }

        public String play()
        {
            readStatus();
            if (state == "stop" || state == "paused")
            {
                callUrl(baseUrl + "requests/status.xml?command=pl_pause&id=4");
                playing = true;
                return "done";
            }
            else
            {
                return "already running";
            }
        }

        public String stop()
        {
            callUrl(baseUrl + "requests/status.xml?command=pl_stop");
            playing = false;
            return "done";
        }

        public String seek(Int32 time)
        {
            callUrl(baseUrl + "requests/status.xml?command=seek&val=" + time);
            return "done";
        }

        public String readStatus()
        {
            var responsecontent = callUrl(baseUrl + "requests/status.xml");

            if (responsecontent == "Unable to connect to the remote server"
                    || responsecontent == "The operation has timed out"
                    || responsecontent == "The request was aborted: The request was canceled.")
            {
                log.Warn("failed to call refresh status: " + responsecontent);
                started = false;
                return responsecontent;
            }

            XmlDocument doc = new XmlDocument();
            doc.LoadXml(responsecontent);

            this.time = Int32.Parse(doc.DocumentElement.SelectSingleNode("/root/time").InnerText);
            this.length = Int32.Parse(doc.DocumentElement.SelectSingleNode("/root/length").InnerText);
            this.state = doc.DocumentElement.SelectSingleNode("/root/state").InnerText;
            this.currentFilename = doc.DocumentElement.SelectSingleNode("/root/information/meta-information").InnerText;


            playing = this.state == "playing";
            log.Info("set playing to : '" + playing + "'");

            var status = "time: " + time + "/" + length + ". state: " + state + " @ '" + currentFilename + "'";

            log.Info("status=" + status);

            started = true;

            return status;
        }


        private String callUrl(String url)
        {
            System.Net.WebRequest req = System.Net.WebRequest.Create(url);

            //log.Info("callUrl: '" + url + "'");

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
                return e.Message;
            }
        }

    }
}
