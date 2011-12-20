using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using log4net.Appender;
using log4net.Core;

namespace MedienverwaltungPlayer
{
    public class MyMemoryAppender : MemoryAppender
    {
        private static MyMemoryAppender instance = null;
        public static MyMemoryAppender getInstance()
        {
            return instance;
        }

        public MyMemoryAppender()
        {
            if (MyMemoryAppender.instance == null)
            {
                MyMemoryAppender.instance = this;
            }
            else
            {
                throw new Exception("singleton!");
            }
        }

        private object _lockObj = new object();

        protected override void Append(LoggingEvent loggingEvent)
        {
            lock (_lockObj)
            {
                base.Append(loggingEvent);
            }
        }

        public LoggingEvent[] ExtractEvents()
        {
            lock (_lockObj)
            {
                LoggingEvent[] events = GetEvents();
                Clear();
                return events;
            }
        }
    }
}
