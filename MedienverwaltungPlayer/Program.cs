using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace MedienverwaltungPlayer
{
    static class Program
    {

        [DllImport("user32.dll")]
        public static extern int SetForegroundWindow(IntPtr hwnd);
        [DllImport("user32.dll")]
        public static extern int IsIconic(IntPtr hwnd);
        [DllImport("user32.dll")]
        public static extern int OpenIcon(IntPtr hwnd);


        /// <summary>
        /// The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            // custom code to prevent this application from running twice.
            // calls SetForeGroundWindow() on already running process window if found and exits
            int ret = 0;
            IntPtr hwndMain;
            Process[] myProcesses = Process.GetProcessesByName(
                Process.GetCurrentProcess().ProcessName);
            foreach (Process p in myProcesses)
            {
                if (p.Id != Process.GetCurrentProcess().Id)
                {
                    hwndMain = p.MainWindowHandle;
                    if (IsIconic(hwndMain) != 0)
                    {  // Fenster minimiert?
                        ret = OpenIcon(hwndMain);
                        if (ret == 0)
                        {
                            throw new Exception(
                    "Error restoring Window from icon");
                        }
                    }
                    ret = SetForegroundWindow(hwndMain);
                    return;
                }
            }
            
            MainForm mainForm = new MainForm();
            mainForm.Show();
            Application.Run();
        }
    }
}
