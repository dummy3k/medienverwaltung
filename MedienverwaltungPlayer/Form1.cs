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

namespace MedienverwaltungPlayer
{
    public partial class Form1 : Form
    {
        VlcPlayer vlcPlayer = new VlcPlayer();

        public Form1()
        {
            InitializeComponent();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            textBox1.Text = vlcPlayer.readStatus();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            textBox1.Text = vlcPlayer.stop();           
        }

        private void button3_Click(object sender, EventArgs e)
        {
            textBox1.Text = vlcPlayer.play();
        }

        private void button4_Click(object sender, EventArgs e)
        {
            textBox1.Text = vlcPlayer.togglePause();
        }

        private void button5_Click(object sender, EventArgs e)
        {
            textBox1.Text = vlcPlayer.start(@"M:\Video\Serien\Southpark\Southpark - Season 01 EN\Southpark - 1x01 - Cartman Gets an Anal Probe.avi");
        }

        private void createPlaylistToolStripMenuItem_Click(object sender, EventArgs e)
        {
            var result = folderBrowserDialog1.ShowDialog();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            Hide();
        }

        private void settingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Show();
        }
    }
}
