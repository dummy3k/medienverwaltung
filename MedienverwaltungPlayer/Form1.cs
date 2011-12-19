using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Xml;
using System.IO;
using log4net;

namespace MedienverwaltungPlayer
{
    public partial class Form1 : Form
    {

        private static log4net.ILog log = log4net.LogManager.GetLogger(System.Reflection.MethodBase.GetCurrentMethod().DeclaringType.ToString() + "." + System.Reflection.MethodBase.GetCurrentMethod().Name);
 
        public PlaylistManager playlistManager;

        public String formatTime(PlaylistEntry entry) {
            if (entry.length == 0)
            {
                return "";
            }

            var percent = Math.Floor(entry.time / entry.length * 100.0);
            return " (" + percent + "%)";
        }

        public String nodeLabel(PlaylistEntry entry)
        {
            var played = entry.path == playlistManager.currentlyPlayedFile() && PlaylistManager.vlcPlayer.playing;
            var time = entry.time > 0 ? formatTime(entry) : "";
            return (played ? "> " : " ") + entry.filename + time;
        }

        public void rebuildTreeNodes()
        {
            treeView1.BeginUpdate();
            treeView1.Nodes.Clear();

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
                    treeView1.Nodes.Add(node);
                }
            }
            else
            {
                treeView1.CheckBoxes = false;

                treeView1.Nodes.Add(new TreeNode("No files in playlist"));
            }

            treeView1.EndUpdate();
        }

        public void updateStatusForm()
        {
            labelFolder.Text = playlistManager.rootFolder;

            treeView1.CheckBoxes = true;

            treeView1.BeginUpdate();

            foreach (TreeNode node in treeView1.Nodes)
            {
                var entry = (PlaylistEntry)node.Tag;
                node.Checked = entry.watched;

                node.Text = nodeLabel(entry);

                if (entry.path == playlistManager.currentlyPlayedFile())
                {
                    node.BackColor = Color.Gray;
                }
                else
                {
                    node.BackColor = Color.Transparent;
                }

            }

            treeView1.EndUpdate();
        }

        public void treeView1_AfterCheck(object sender, TreeViewEventArgs e)
        {
            var entry = (PlaylistEntry)e.Node.Tag;
            entry.watched = e.Node.Checked;
        }

        public void selectFolder()
        {
            folderBrowserDialog1.Description = "Select base folder for playlist";
            folderBrowserDialog1.SelectedPath = @"M:\Video\Dexter Season 1";
            folderBrowserDialog1.ShowDialog();
            
            String path = folderBrowserDialog1.SelectedPath;

            //String name = Microsoft.VisualBasic.Interaction.InputBox("Name?", "Name?", "Playlist 1", 0, 0);
            Playlist playlist = new Playlist(path, "playlist");

            playlistManager.currentPlaylist = null;
            playlistManager.playlists.Clear();
            playlistManager.playlists.Add(playlist);
            playlistManager.rootFolder = path;

            rebuildTreeNodes();
            updateStatusForm();
        }

        public void play()
        {
            playlistManager.play();
            updateStatusForm();
        }

        public void stop()
        {
            playlistManager.stop();
            updateStatusForm();
        }

        public void pause()
        {
            playlistManager.pause();
            updateStatusForm();
        }

        public void next()
        {

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


        public Form1()
        {
            InitializeComponent();

            log4net.Config.XmlConfigurator.Configure();

            var appData = System.Environment.GetEnvironmentVariable("APPDATA");

            var settingsFolder = Path.Combine(appData, "mvPlayer");
            var settingsFile = Path.Combine(settingsFolder, "playlists.data");

            if (!File.Exists(settingsFolder))
            {
                Directory.CreateDirectory(settingsFolder);
            }

            if (File.Exists(settingsFile))
            {
                playlistManager = PlaylistManager.load(settingsFile);
                rebuildTreeNodes();
                updateStatusForm();
            }
            else
            {
                playlistManager = new PlaylistManager();
                labelFolder.Text = "no folder selected";
            }
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Hide();
            PlaylistManager.vlcPlayer.readStatus();
        }


        private void settingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            updateStatusForm();
            Show();
        }

        private void createPlaylistToolStripMenuItem_Click(object sender, EventArgs e)
        {
            selectFolder();
        }

        private void playToolStripMenuItem_Click(object sender, EventArgs e)
        {
            play();
        }

        private void exitToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void nextToolStripMenuItem_Click(object sender, EventArgs e)
        {
            next();
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

        
        /*
        private void button7_Click(object sender, EventArgs e)
        {
            var currentlyPlayedFile = playlistManager.currentlyPlayedFile();

            foreach (var playlist in playlistManager.playlists)
            {
//                textBox1.Text += playlist.name + " (" + playlist.rootPath + ")\r\n\r\n";
                foreach (var entry in playlist.playlistEntries)
                {
                    var info = new FileInfo(entry.path);
  //                  textBox1.Text += " - " + info.Name + " " + (entry.watched ? " (watched)" : "") + (entry.path == currentlyPlayedFile ? " PLAYING" : "") + " @ " + entry.time + "\r\n";
                }
            }
        }
         * */

        private void timer1_Tick(object sender, EventArgs e)
        {
            timer1.Enabled = false;
            playlistManager.update();
            updateStatusForm();
            timer1.Enabled = true;
        }

        private void Form1_FormClosed(object sender, FormClosedEventArgs e)
        {
            PlaylistManager.vlcPlayer.stop();

            var appData = System.Environment.GetEnvironmentVariable("APPDATA");

            var settingsFolder = Path.Combine(appData, "mvPlayer");
            var settingsFile = Path.Combine(settingsFolder, "playlists.data");

            if (!File.Exists(settingsFolder))
            {
                Directory.CreateDirectory(settingsFolder);
            }

            playlistManager.save(settingsFile);
            log.Info("saved settings");
        }

        private void button1_Click_1(object sender, EventArgs e)
        {
            selectFolder();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            pause();
        }

        private void button3_Click(object sender, EventArgs e)
        {
            next();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            prev();
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
        }


    }
}
