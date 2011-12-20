using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Linq;
using System.Windows.Forms;
using System.Xml;
using System.IO;
using log4net;
using System.Threading;
using log4net.Core;
using System.Runtime.InteropServices;

namespace MedienverwaltungPlayer
{
    public partial class MainForm : Form
    {
        #region ### members ################################################

            private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);
 
            private PlaylistManager playlistManager = null;
            private Boolean shutdown = false;
            private Playlist comboBoxPlaylistLastSelected = null;

            private Icon iconPlay = null;
            private Icon iconStop = null;

            private Int32 ticks = 1;

            [DllImport("user32.dll")]
            public static extern int SetForegroundWindow(IntPtr hwnd);

            [DllImport("user32.dll")]
            static extern bool LockWindowUpdate(IntPtr hWndLock);

        #endregion
        #region ### logwatcher #############################################
        /*
            private bool logWatching = true;
            private Thread logWatcher;


            #region thread-safe mLog.clear() = ThreadSafeClearLog#################################################
            // This delegate enables asynchronous calls for setting
            // the text property on a TextBox control.
            delegate void ThreadSafeClearLogCallback();
            private void ThreadSafeClearLog()
            {
                this.ClearLog();
            }
            private void ClearLog()
            {
                if (this.mLog.InvokeRequired)
                {
                    ThreadSafeClearLogCallback d = new ThreadSafeClearLogCallback(ClearLog);
                    this.Invoke(d, new object[] { });
                }
                else
                {
                    this.mLog.Clear();
                }

            }
            #endregion

            #region thread-safe mLog.clear() = ThreadSafeAppendLog#################################################
            // This delegate enables asynchronous calls for setting
            // the text property on a TextBox control.
            delegate void ThreadSafeAppendLogCallback(String txt);
            private void ThreadSafeAppendLog(String txt)
            {
                this.AppendLog(txt);
            }
            private void AppendLog(String txt)
            {
                if (this.mLog.InvokeRequired)
                {
                    ThreadSafeAppendLogCallback d = new ThreadSafeAppendLogCallback(AppendLog);
                    this.Invoke(d, new object[] { txt });
                }
                else
                {
                    this.mLog.AppendText(txt);
                }

            }
            #endregion

            private void LogWatcher()
            {
                // we loop until the Form is closed  
                while (logWatching)
                {
                    var memoryLogger = MyMemoryAppender.getInstance();
                    LoggingEvent[] events = null;

                    if (memoryLogger != null)
                    {
                        events = memoryLogger.ExtractEvents();    
                    }
                    
                    if (events != null && events.Length > 0)
                    {
                        // if there are events, we clear them from the logger,  
                        // since we're done with them  
                        memoryLogger.Clear();
                        foreach (LoggingEvent ev in events)
                        {
                            StringBuilder builder;
                            // the line we want to log  
                            string line = ev.LoggerName + ": " + ev.RenderedMessage + "\r\n";
                            // don't want to grow this log indefinetly, so limit to 100 lines  
                            if (mLog.Lines.Length > 99)
                            {
                                try
                                {
                                    builder = new StringBuilder(mLog.Text);
                                    // strip out a nice chunk from the beginning  
                                    builder.Remove(0, mLog.Text.IndexOf('\r', 3000) + 2);
                                    builder.Append(line);
                                    ThreadSafeClearLog();
                                    // using AppendText since that makes sure the TextBox stays 
                                    // scrolled at the bottom 
                                    ThreadSafeAppendLog(builder.ToString());
                                }
                                catch (Exception)
                                {
                                }
                            }
                            else
                            {
                                ThreadSafeAppendLog(line);
                            }
                        }
                    }
                    // nap for a while, don't need the events on the millisecond.  
                    Thread.Sleep(500);
                }
            }  
        
         */
        #endregion
        #region ### business methods #######################################

        public void save()
        {
            var settingsFolder = Path.Combine(Environment.GetFolderPath(
                    Environment.SpecialFolder.LocalApplicationData), "mvPlayer");
            var settingsFile = Path.Combine(settingsFolder, "playlists.data");

            if (!File.Exists(settingsFolder))
            {
                Directory.CreateDirectory(settingsFolder);
            }

            playlistManager.save(settingsFile);
            log.Info("saved settings");
        }

        public void onPlayingChange(Boolean playing)
        {
            if (playing)
            {
                this.notifyIcon1.Icon = iconPlay;
                this.Icon = iconPlay;
            }
            else
            {
                this.notifyIcon1.Icon = iconStop;
                this.Icon = iconStop;
            }

        }

        public String formatTime(PlaylistEntry entry) {
            if (entry.length == 0)
            {
                return "";
            }

            var percent = Math.Floor((double)entry.time / (double)entry.length * 100.0);

            var minutes = entry.time / 60;
            var seconds = entry.time % 60;

            return String.Format(" ({0:00}:{1:00} or {2:0}%)", minutes, seconds, percent);
        }

        public String nodeLabel(PlaylistEntry entry)
        {
            var time = entry.time > 0 ? formatTime(entry) : "";
            return entry.filename + time;
        }

        public void removeCurrentlySelectedEntry()
        {
            if (this.treeViewPlaylistEntries.SelectedNode != null)
            {
                var entry = (PlaylistEntry)this.treeViewPlaylistEntries.SelectedNode.Tag;

                if (entry != null && playlistManager.currentPlaylist != null)
                {
                    playlistManager.currentPlaylist.deleteEntry(entry);
                    rebuildTreeNodes();
                }

            }
        }

        public void deleteCurrentPlaylist()
        {
            playlistManager.deleteCurrentPlaylist();
            comboBoxPlaylistLastSelected = null;
            updatePlaylistComboBox();
            rebuildTreeNodes();
        }

        public void check()
        {
            if (playlistManager.currentPlaylist != null)
            {
                playlistManager.currentPlaylist.check();
                updateStatusForm();
            }
        }

        public void exit()
        {
            shutdown = true;
            Close();
            Application.Exit();
        }

        public void rebuildTreeNodes()
        {
            treeViewPlaylistEntries.BeginUpdate();
            //LockWindowUpdate(treeViewPlaylistEntries.Handle);
            treeViewPlaylistEntries.Nodes.Clear();

            if (playlistManager.currentPlaylist == null)
            {
                playlistManager.currentPlaylist = playlistManager.playlists.FirstOrDefault();
            }

            if (playlistManager.currentPlaylist != null)
            {
                foreach (var entry in playlistManager.currentPlaylist.playlistEntries)
                {
                    var node = new TreeNode(nodeLabel(entry));
                    node.Checked = entry.watched;
                    node.Tag = entry;
                    treeViewPlaylistEntries.Nodes.Add(node);
                }
            }
            else
            {
                treeViewPlaylistEntries.CheckBoxes = false;

                treeViewPlaylistEntries.Nodes.Add(new TreeNode("No files in playlist"));
            }

            //LockWindowUpdate(IntPtr.Zero);
            treeViewPlaylistEntries.EndUpdate();
            updateStatusForm();
        }

        public Boolean checkVlcLocation()
        {
            // check for vlc binary
            if (File.Exists(PlaylistManager.vlcPlayer.vlcLocation) == false)
            {
                var vlcProcess = PlaylistManager.vlcPlayer.findRunningVlcProcess();

                if (vlcProcess != null && File.Exists(vlcProcess.MainModule.FileName))
                {
                    PlaylistManager.vlcPlayer.vlcLocation = vlcProcess.MainModule.FileName;
                    return true;
                }

                return selectVlcLocation();
            }

            return true;
        }

        public Boolean selectVlcLocation()
        {
            openFileDialog1.CheckFileExists = true;
            if (openFileDialog1.ShowDialog() != DialogResult.OK) return false;

            PlaylistManager.vlcPlayer.vlcLocation = openFileDialog1.FileName;
            return true;

        }

        public void updatePlaylistComboBox()
        {

            comboBoxPlaylists.BeginUpdate();
            //LockWindowUpdate(comboBoxPlaylists.Handle);
            comboBoxPlaylists.Items.Clear();
            foreach (var playlist in playlistManager.playlists)
            {
                var item = playlist;
                comboBoxPlaylists.Items.Add(item);
            }
            //LockWindowUpdate(IntPtr.Zero);
            comboBoxPlaylists.EndUpdate();

            if (playlistManager.currentPlaylist != null)
            {
                comboBoxPlaylists.SelectedItem = playlistManager.currentPlaylist;
            }
            else
            {
                comboBoxPlaylists.SelectedItem = null;
                comboBoxPlaylists.Text = "";
            }
        }

        public void updateStatusForm()
        {
            if (this.Visible == false) return;

            labelFolder.Text = playlistManager.rootFolder;

            //if (playlistManager.currentPlaylist != null && playlistManager.currentPlaylist.currentPlaylistEntry != null)
            {
                //labelFile.Text = playlistManager.currentPlaylist.currentPlaylistEntry.filename;
                labelFile.Text = PlaylistManager.vlcPlayer.currentFilename;
            }
            /*else
            {
                labelFile.Text = "no folder selected";
            }*/


            treeViewPlaylistEntries.CheckBoxes = true;


            treeViewPlaylistEntries.BeginUpdate();

            foreach (TreeNode node in treeViewPlaylistEntries.Nodes)
            {
                var entry = (PlaylistEntry)node.Tag;
                if (entry == null) continue; 

                node.Checked = entry.watched;

                var playedFile = playlistManager.currentlyPlayedFile();

                Boolean bold = false;
                Boolean red = false;

                if (PlaylistManager.vlcPlayer.playing && playedFile != null && entry.filename == new FileInfo(playedFile).Name)
                {
                    bold = true;
                }

                if (entry.fileNotFound)
                {
                    red = true;
                }


                if (bold)
                {
                    node.NodeFont = new Font(treeViewPlaylistEntries.Font, FontStyle.Bold);
                }
                else
                {
                    node.NodeFont = new Font(treeViewPlaylistEntries.Font, FontStyle.Regular);
                }

                if (red)
                {
                    node.ForeColor = Color.Red;
                }
                else
                {
                    node.ForeColor = Color.Black;
                }




                node.Text = nodeLabel(entry);
            }

            treeViewPlaylistEntries.EndUpdate();
        }

        public void updateTooltip()
        {
            if(playlistManager.currentlyPlayedFile() != null) {
                var fileName = new FileInfo(playlistManager.currentlyPlayedFile()).Name;

                var msg = "'" + fileName.Substring(0, Math.Min(30, fileName.Length)) + (fileName.Length > 30 ? "..." : "") + "'" + formatTime(playlistManager.currentPlaylist.currentPlaylistEntry);

                if (PlaylistManager.vlcPlayer.playing)
                {
                    notifyIcon1.Text = "playing " + msg;
                }
                else
                {
                    if (PlaylistManager.vlcPlayer.state == "paused")
                    {
                        notifyIcon1.Text = "paused " + msg;
                    }
                    else
                    {
                        notifyIcon1.Text = "stopped " + msg;
                    }
                }
            }
            
        }

        public void createNewPlaylistFromFolderSelection()
        {
            folderBrowserDialog1.Description = "Select base folder for new playlist";
            
            if (folderBrowserDialog1.ShowDialog() != DialogResult.OK) return;
            
            String path = folderBrowserDialog1.SelectedPath;

            Playlist playlist = new Playlist(path, new FileInfo(path).Name);

            playlistManager.playlists.Add(playlist);
            playlistManager.rootFolder = path;
            playlistManager.currentPlaylist = playlist;

            updatePlaylistComboBox();
            rebuildTreeNodes();
        }

        public void play()
        {
            if (!checkVlcLocation()) return;
            playlistManager.play();
            updateStatusForm();
        }

        public void pause()
        {
            if (!checkVlcLocation()) return;
            playlistManager.pause();
            updateStatusForm();
        }

        public void stop()
        {
            if (!checkVlcLocation()) return;
            playlistManager.stop();
            updateStatusForm();
        }
        
        public void next()
        {
            if (!checkVlcLocation()) return;
            playlistManager.next();
            var nextFile = playlistManager.currentlyPlayedFile();

            if (nextFile != null)
            {
                var filename = new FileInfo(nextFile).Name;
                notifyIcon1.BalloonTipText = "Next: " + filename;
                notifyIcon1.ShowBalloonTip(5000);
            }
            else
            {
                notifyIcon1.BalloonTipText = "No more files to play";
                notifyIcon1.ShowBalloonTip(5000);
            }
            updateStatusForm();
        }

        public void prev()
        {
            if (!checkVlcLocation()) return;
            playlistManager.prev();

            var prevFile = playlistManager.currentlyPlayedFile();

            if (prevFile != null)
            {
                var filename = new FileInfo(prevFile).Name;
                notifyIcon1.BalloonTipText = "Prev: " + filename;
                notifyIcon1.ShowBalloonTip(3000);
            }
            else
            {
                notifyIcon1.BalloonTipText = "No more files to play";
                notifyIcon1.ShowBalloonTip(3000);
            }
            updateStatusForm();
        }

        #endregion
        #region ### lifecycle methods ######################################

        public MainForm()
        {
            InitializeComponent();

            /*
            // Since there are no events to catch on logging, we dedicate  
            // a thread to watching for logging events  
            logWatcher = new Thread(new ThreadStart(LogWatcher));
            logWatcher.Start();  
            */

            log4net.Config.XmlConfigurator.Configure();
            VlcPlayer.mainForm = this;

            iconPlay = this.notifyIcon1.Icon;
            iconStop = this.Icon;
            
            onPlayingChange(false);

            var settingsFolder = Path.Combine(Environment.GetFolderPath(
                        Environment.SpecialFolder.LocalApplicationData), "mvPlayer");
            var settingsFile = Path.Combine(settingsFolder, "playlists.data");

            if (!File.Exists(settingsFolder))
            {
                Directory.CreateDirectory(settingsFolder);
            }

            if (File.Exists(settingsFile))
            {
                playlistManager = PlaylistManager.load(settingsFile);
                PlaylistManager.vlcPlayer = playlistManager._vlcPlayer;
                PlaylistManager.vlcPlayer.resetStatus();
                rebuildTreeNodes();
            }
            else
            {
                playlistManager = PlaylistManager.getInstance();
                labelFolder.Text = "no folder selected";
                labelFile.Text = "no file selected";
            }

            /*
            System.Reflection.PropertyInfo aProp = typeof(System.Windows.Forms.Control)
                    .GetProperty("DoubleBuffered", System.Reflection.BindingFlags.NonPublic |
                    System.Reflection.BindingFlags.Instance);
                                aProp.SetValue(treeViewPlaylistEntries, true, null);
            */


            playlistManager.select();
            updatePlaylistComboBox();
        }

        private void MainForm_Load(object sender, EventArgs e)
        {
            Show();
            if (checkVlcLocation())
            {
                PlaylistManager.vlcPlayer.readStatus();
            }
        }

        private void MainForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            if (shutdown == false)
            {
                e.Cancel = true;
            }
            Hide();

            // Gotta stop our logging thread  
            /*
            logWatching = false;
            logWatcher.Join();  
            */
        }

        private void MainForm_FormClosed(object sender, FormClosedEventArgs e)
        {
            PlaylistManager.vlcPlayer.stop();

            save();

            PlaylistManager.vlcPlayer.destory();
        }

        #endregion
        #region ### events #################################################

        private void settingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            updateStatusForm();
            Show();
        }

        private void createPlaylistToolStripMenuItem_Click(object sender, EventArgs e)
        {
            createNewPlaylistFromFolderSelection();
        }

        private void playToolStripMenuItem_Click(object sender, EventArgs e)
        {
            play();
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            exit();
        }

        private void statusToolStripMenuItem_Click(object sender, EventArgs e)
        {
            this.Show();
        }

        private void stopToolStripMenuItem_Click(object sender, EventArgs e)
        {
            stop();
        }

        private void pauseToolStripMenuItem_Click(object sender, EventArgs e)
        {
            pause();
        }

        private void prevToolStripMenuItem_Click(object sender, EventArgs e)
        {
            prev();
        }

        private void nextToolStripMenuItem_Click(object sender, EventArgs e)
        {
            next();
        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            timer1.Enabled = false;
            playlistManager.update();
            updateStatusForm();
            updateTooltip();
            
            ticks++;

            if (ticks % 30 == 0)
            {
                save();
            }

            timer1.Enabled = true;
        }

        private void buttonSelectFolder_Click(object sender, EventArgs e)
        {
            createNewPlaylistFromFolderSelection();
        }

        public void treeView1_AfterCheck(object sender, TreeViewEventArgs e)
        {
            var entry = (PlaylistEntry)e.Node.Tag;

            if (entry != null)
            {
                entry.watched = e.Node.Checked;
            }
        }

        private void treeView1_NodeMouseDoubleClick(object sender, TreeNodeMouseClickEventArgs e)
        {
            var entry = (PlaylistEntry)e.Node.Tag;

            playlistManager.currentPlaylist.play(entry);

            updateStatusForm();
        }
        
        private void notifyIcon1_MouseDoubleClick(object sender, MouseEventArgs e)
        {
            updateStatusForm();
            Show();

            try
            {
                SetForegroundWindow(this.Handle);
            }
            catch (Exception)
            {
                
                // ignore for linux/mono compatibility
            }
        }

        private void buttonPlay_Click(object sender, EventArgs e)
        {
            play();
        }

        private void buttonNext_Click(object sender, EventArgs e)
        {
            next();
        }

        private void buttonPrev_Click(object sender, EventArgs e)
        {
            prev();
        }

        private void buttonStatus_Click(object sender, EventArgs e)
        {
            stop();
        }

        private void buttonPause_Click(object sender, EventArgs e)
        {
            pause();
        }

        private void comboBoxPlaylists_SelectedValueChanged(object sender, EventArgs e)
        {
            if (comboBoxPlaylists.SelectedItem != null)
            {
                var playlist = (Playlist)comboBoxPlaylists.SelectedItem;
                playlistManager.select(playlist);

                rebuildTreeNodes();
            }
        }

        private void comboBoxPlaylists_TextChanged(object sender, EventArgs e)
        {
            if (comboBoxPlaylists.SelectedItem != null)
            {
                var playlist = (Playlist)comboBoxPlaylists.SelectedItem;
                comboBoxPlaylistLastSelected = playlist;
            }
            else if (comboBoxPlaylistLastSelected != null)
            {
                comboBoxPlaylistLastSelected.name = comboBoxPlaylists.Text;
            }
        }

        private void comboBoxPlaylists_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter || e.KeyCode == Keys.Return)
            {
                updatePlaylistComboBox();
            }
        }

        private void toolStripButtonImportFromFolder_Click(object sender, EventArgs e)
        {
            createNewPlaylistFromFolderSelection();
        }

        private void toolStripButtonDeleteCurrentPlaylist_Click(object sender, EventArgs e)
        {
            deleteCurrentPlaylist();
        }

        private void buttonExit_Click(object sender, EventArgs e)
        {
            exit();
        }

        private void toolStripButtonCheckFiles_Click(object sender, EventArgs e)
        {
            check();
        }

        private void treeViewPlaylistEntries_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Delete || e.KeyCode == Keys.Clear)
            {
                removeCurrentlySelectedEntry();
            }
        }

        private void toolStripMenuItem1_Click(object sender, EventArgs e)
        {
            play();
        }

        #endregion

    }
}
