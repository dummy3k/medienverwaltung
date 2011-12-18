using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Xml;
using System.Diagnostics;

namespace MedienverwaltungPlayer
{
    class VlcPlayer
    {
        public String baseUrl { get; set; }
        public Int32 time { get; set; }
        public Int32 length { get; private set; }
        public String state { get; private set; }
        public String currentFilename { get; set; }


        public VlcPlayer(String baseUrl = "http://localhost:8080/")
        {
            this.baseUrl = baseUrl;
        }

        public String togglePause()
        {
            callUrl(baseUrl + "requests/status.xml?command=pl_pause");
            return "done";
        }

        public String start(String filenameAbsolute) {
            String vlcExe = @"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe";

            String filename = new System.IO.FileInfo(filenameAbsolute).Name;

            readStatus();

            if (currentFilename == filename)
            {
                play();
                return "already running";
            }
            String paramList = "--control=http";

            Process.Start(vlcExe, paramList + " \"" + filenameAbsolute + "\"");

            return "done";
        }

        public String play()
        {
            readStatus();
            if (state == "stop" || state == "paused")
            {
                callUrl(baseUrl + "requests/status.xml?command=pl_pause&id=4");
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
            return "done";
        }

        public String readStatus()
        {
            var responsecontent = callUrl(baseUrl + "requests/status.xml");
            
            XmlDocument doc = new XmlDocument();
            doc.LoadXml(responsecontent);

            this.time = Int32.Parse(doc.DocumentElement.SelectSingleNode("/root/time").InnerText);
            this.length = Int32.Parse(doc.DocumentElement.SelectSingleNode("/root/length").InnerText);
            this.state = doc.DocumentElement.SelectSingleNode("/root/state").InnerText;
            this.currentFilename = doc.DocumentElement.SelectSingleNode("/root/information/meta-information").InnerText;

            return "time: " + time + "/" + length + ". state: " + state + " @ '" + currentFilename + "'";
        }


        private String callUrl(String url) {
            System.Net.WebRequest req = System.Net.WebRequest.Create(url);

            req.ContentType = "text/xml";
            req.Method = "GET";

            System.Net.WebResponse resp = req.GetResponse();
            if (resp == null) return null;
            System.IO.StreamReader sr = new System.IO.StreamReader(resp.GetResponseStream());

            var responsecontent = sr.ReadToEnd().Trim();
            return responsecontent;
        }

    }
}
