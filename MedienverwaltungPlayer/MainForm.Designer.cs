namespace MedienverwaltungPlayer
{
    partial class MainForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.Windows.Forms.Label label1;
            System.Windows.Forms.Label label2;
            System.Windows.Forms.Label label3;
            System.Windows.Forms.Label label4;
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(MainForm));
            this.notifyIcon1 = new System.Windows.Forms.NotifyIcon(this.components);
            this.contextMenuStrip1 = new System.Windows.Forms.ContextMenuStrip(this.components);
            this.toolStripMenuItem1 = new System.Windows.Forms.ToolStripMenuItem();
            this.pauseToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.stopToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.toolStripMenuItem2 = new System.Windows.Forms.ToolStripMenuItem();
            this.prevToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.exitToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.folderBrowserDialog1 = new System.Windows.Forms.FolderBrowserDialog();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.labelFolder = new System.Windows.Forms.Label();
            this.buttonPlay = new System.Windows.Forms.Button();
            this.buttonNext = new System.Windows.Forms.Button();
            this.buttonPrev = new System.Windows.Forms.Button();
            this.buttonStop = new System.Windows.Forms.Button();
            this.buttonPause = new System.Windows.Forms.Button();
            this.treeViewPlaylistEntries = new System.Windows.Forms.TreeView();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.comboBoxPlaylists = new System.Windows.Forms.ComboBox();
            this.toolStrip2 = new System.Windows.Forms.ToolStrip();
            this.toolStripButtonImportFromFolder = new System.Windows.Forms.ToolStripButton();
            this.toolStripButtonDeleteCurrentPlaylist = new System.Windows.Forms.ToolStripButton();
            this.toolStripButtonCheckFiles = new System.Windows.Forms.ToolStripButton();
            this.buttonExit = new System.Windows.Forms.Button();
            this.labelFile = new System.Windows.Forms.Label();
            label1 = new System.Windows.Forms.Label();
            label2 = new System.Windows.Forms.Label();
            label3 = new System.Windows.Forms.Label();
            label4 = new System.Windows.Forms.Label();
            this.contextMenuStrip1.SuspendLayout();
            this.toolStrip2.SuspendLayout();
            this.SuspendLayout();
            // 
            // label1
            // 
            label1.AutoSize = true;
            label1.Location = new System.Drawing.Point(9, 49);
            label1.Name = "label1";
            label1.Size = new System.Drawing.Size(39, 13);
            label1.TabIndex = 1;
            label1.Text = "Folder:";
            // 
            // label2
            // 
            label2.AutoSize = true;
            label2.Location = new System.Drawing.Point(9, 99);
            label2.Name = "label2";
            label2.Size = new System.Drawing.Size(42, 13);
            label2.TabIndex = 5;
            label2.Text = "Playlist:";
            // 
            // label3
            // 
            label3.AutoSize = true;
            label3.Location = new System.Drawing.Point(9, 17);
            label3.Name = "label3";
            label3.Size = new System.Drawing.Size(48, 13);
            label3.TabIndex = 17;
            label3.Text = "Controls:";
            // 
            // label4
            // 
            label4.AutoSize = true;
            label4.Location = new System.Drawing.Point(9, 72);
            label4.Name = "label4";
            label4.Size = new System.Drawing.Size(29, 13);
            label4.TabIndex = 22;
            label4.Text = "File: ";
            // 
            // notifyIcon1
            // 
            this.notifyIcon1.ContextMenuStrip = this.contextMenuStrip1;
            this.notifyIcon1.Icon = ((System.Drawing.Icon)(resources.GetObject("notifyIcon1.Icon")));
            this.notifyIcon1.Text = "notifyIcon1";
            this.notifyIcon1.Visible = true;
            this.notifyIcon1.MouseDoubleClick += new System.Windows.Forms.MouseEventHandler(this.notifyIcon1_MouseDoubleClick);
            // 
            // contextMenuStrip1
            // 
            this.contextMenuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripMenuItem1,
            this.pauseToolStripMenuItem,
            this.stopToolStripMenuItem,
            this.toolStripMenuItem2,
            this.prevToolStripMenuItem,
            this.exitToolStripMenuItem});
            this.contextMenuStrip1.Name = "contextMenuStrip1";
            this.contextMenuStrip1.Size = new System.Drawing.Size(120, 136);
            // 
            // toolStripMenuItem1
            // 
            this.toolStripMenuItem1.Name = "toolStripMenuItem1";
            this.toolStripMenuItem1.Size = new System.Drawing.Size(119, 22);
            this.toolStripMenuItem1.Text = "Play";
            this.toolStripMenuItem1.Click += new System.EventHandler(this.toolStripMenuItem1_Click);
            // 
            // pauseToolStripMenuItem
            // 
            this.pauseToolStripMenuItem.Name = "pauseToolStripMenuItem";
            this.pauseToolStripMenuItem.Size = new System.Drawing.Size(119, 22);
            this.pauseToolStripMenuItem.Text = "Pause";
            this.pauseToolStripMenuItem.Click += new System.EventHandler(this.pauseToolStripMenuItem_Click);
            // 
            // stopToolStripMenuItem
            // 
            this.stopToolStripMenuItem.Name = "stopToolStripMenuItem";
            this.stopToolStripMenuItem.Size = new System.Drawing.Size(119, 22);
            this.stopToolStripMenuItem.Text = "Stop";
            this.stopToolStripMenuItem.Click += new System.EventHandler(this.stopToolStripMenuItem_Click);
            // 
            // toolStripMenuItem2
            // 
            this.toolStripMenuItem2.Name = "toolStripMenuItem2";
            this.toolStripMenuItem2.Size = new System.Drawing.Size(119, 22);
            this.toolStripMenuItem2.Text = "Next";
            this.toolStripMenuItem2.Click += new System.EventHandler(this.nextToolStripMenuItem_Click);
            // 
            // prevToolStripMenuItem
            // 
            this.prevToolStripMenuItem.Name = "prevToolStripMenuItem";
            this.prevToolStripMenuItem.Size = new System.Drawing.Size(119, 22);
            this.prevToolStripMenuItem.Text = "Previous";
            this.prevToolStripMenuItem.Click += new System.EventHandler(this.prevToolStripMenuItem_Click);
            // 
            // exitToolStripMenuItem
            // 
            this.exitToolStripMenuItem.Name = "exitToolStripMenuItem";
            this.exitToolStripMenuItem.Size = new System.Drawing.Size(119, 22);
            this.exitToolStripMenuItem.Text = "Exit";
            this.exitToolStripMenuItem.Click += new System.EventHandler(this.exitToolStripMenuItem_Click);
            // 
            // folderBrowserDialog1
            // 
            this.folderBrowserDialog1.ShowNewFolderButton = false;
            // 
            // timer1
            // 
            this.timer1.Enabled = true;
            this.timer1.Interval = 1000;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // labelFolder
            // 
            this.labelFolder.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.labelFolder.Location = new System.Drawing.Point(62, 49);
            this.labelFolder.Name = "labelFolder";
            this.labelFolder.Size = new System.Drawing.Size(399, 18);
            this.labelFolder.TabIndex = 3;
            this.labelFolder.Text = "no folder selected";
            // 
            // buttonPlay
            // 
            this.buttonPlay.Location = new System.Drawing.Point(62, 12);
            this.buttonPlay.Name = "buttonPlay";
            this.buttonPlay.Size = new System.Drawing.Size(51, 23);
            this.buttonPlay.TabIndex = 6;
            this.buttonPlay.Text = "play";
            this.buttonPlay.UseVisualStyleBackColor = true;
            this.buttonPlay.Click += new System.EventHandler(this.buttonPlay_Click);
            // 
            // buttonNext
            // 
            this.buttonNext.Location = new System.Drawing.Point(119, 12);
            this.buttonNext.Name = "buttonNext";
            this.buttonNext.Size = new System.Drawing.Size(52, 23);
            this.buttonNext.TabIndex = 7;
            this.buttonNext.Text = "next";
            this.buttonNext.UseVisualStyleBackColor = true;
            this.buttonNext.Click += new System.EventHandler(this.buttonNext_Click);
            // 
            // buttonPrev
            // 
            this.buttonPrev.Location = new System.Drawing.Point(177, 12);
            this.buttonPrev.Name = "buttonPrev";
            this.buttonPrev.Size = new System.Drawing.Size(60, 23);
            this.buttonPrev.TabIndex = 8;
            this.buttonPrev.Text = "previous";
            this.buttonPrev.UseVisualStyleBackColor = true;
            this.buttonPrev.Click += new System.EventHandler(this.buttonPrev_Click);
            // 
            // buttonStop
            // 
            this.buttonStop.Location = new System.Drawing.Point(243, 12);
            this.buttonStop.Name = "buttonStop";
            this.buttonStop.Size = new System.Drawing.Size(75, 23);
            this.buttonStop.TabIndex = 14;
            this.buttonStop.Text = "stop";
            this.buttonStop.UseVisualStyleBackColor = true;
            this.buttonStop.Click += new System.EventHandler(this.buttonStatus_Click);
            // 
            // buttonPause
            // 
            this.buttonPause.Location = new System.Drawing.Point(324, 12);
            this.buttonPause.Name = "buttonPause";
            this.buttonPause.Size = new System.Drawing.Size(75, 23);
            this.buttonPause.TabIndex = 15;
            this.buttonPause.Text = "pause";
            this.buttonPause.UseVisualStyleBackColor = true;
            this.buttonPause.Click += new System.EventHandler(this.buttonPause_Click);
            // 
            // treeViewPlaylistEntries
            // 
            this.treeViewPlaylistEntries.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
            | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.treeViewPlaylistEntries.Location = new System.Drawing.Point(9, 148);
            this.treeViewPlaylistEntries.Name = "treeViewPlaylistEntries";
            this.treeViewPlaylistEntries.Size = new System.Drawing.Size(449, 331);
            this.treeViewPlaylistEntries.TabIndex = 16;
            this.treeViewPlaylistEntries.AfterCheck += new System.Windows.Forms.TreeViewEventHandler(this.treeView1_AfterCheck);
            this.treeViewPlaylistEntries.NodeMouseDoubleClick += new System.Windows.Forms.TreeNodeMouseClickEventHandler(this.treeView1_NodeMouseDoubleClick);
            this.treeViewPlaylistEntries.KeyDown += new System.Windows.Forms.KeyEventHandler(this.treeViewPlaylistEntries_KeyDown);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.DefaultExt = "exe";
            this.openFileDialog1.FileName = "openFileDialog1";
            this.openFileDialog1.Title = "VLC binary not found! Please select vlc.exe";
            // 
            // comboBoxPlaylists
            // 
            this.comboBoxPlaylists.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.comboBoxPlaylists.FormattingEnabled = true;
            this.comboBoxPlaylists.Location = new System.Drawing.Point(62, 96);
            this.comboBoxPlaylists.Name = "comboBoxPlaylists";
            this.comboBoxPlaylists.Size = new System.Drawing.Size(399, 21);
            this.comboBoxPlaylists.TabIndex = 18;
            this.comboBoxPlaylists.SelectedValueChanged += new System.EventHandler(this.comboBoxPlaylists_SelectedValueChanged);
            this.comboBoxPlaylists.TextChanged += new System.EventHandler(this.comboBoxPlaylists_TextChanged);
            this.comboBoxPlaylists.KeyDown += new System.Windows.Forms.KeyEventHandler(this.comboBoxPlaylists_KeyDown);
            // 
            // toolStrip2
            // 
            this.toolStrip2.Dock = System.Windows.Forms.DockStyle.None;
            this.toolStrip2.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.toolStripButtonImportFromFolder,
            this.toolStripButtonDeleteCurrentPlaylist,
            this.toolStripButtonCheckFiles});
            this.toolStrip2.Location = new System.Drawing.Point(9, 120);
            this.toolStrip2.Name = "toolStrip2";
            this.toolStrip2.Size = new System.Drawing.Size(359, 25);
            this.toolStrip2.TabIndex = 20;
            this.toolStrip2.Text = "toolStrip2";
            // 
            // toolStripButtonImportFromFolder
            // 
            this.toolStripButtonImportFromFolder.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.toolStripButtonImportFromFolder.Image = ((System.Drawing.Image)(resources.GetObject("toolStripButtonImportFromFolder.Image")));
            this.toolStripButtonImportFromFolder.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolStripButtonImportFromFolder.Name = "toolStripButtonImportFromFolder";
            this.toolStripButtonImportFromFolder.Size = new System.Drawing.Size(175, 22);
            this.toolStripButtonImportFromFolder.Text = "import new playlist from folder";
            this.toolStripButtonImportFromFolder.Click += new System.EventHandler(this.toolStripButtonImportFromFolder_Click);
            // 
            // toolStripButtonDeleteCurrentPlaylist
            // 
            this.toolStripButtonDeleteCurrentPlaylist.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.toolStripButtonDeleteCurrentPlaylist.Image = ((System.Drawing.Image)(resources.GetObject("toolStripButtonDeleteCurrentPlaylist.Image")));
            this.toolStripButtonDeleteCurrentPlaylist.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolStripButtonDeleteCurrentPlaylist.Name = "toolStripButtonDeleteCurrentPlaylist";
            this.toolStripButtonDeleteCurrentPlaylist.Size = new System.Drawing.Size(124, 22);
            this.toolStripButtonDeleteCurrentPlaylist.Text = "delete current playlist";
            this.toolStripButtonDeleteCurrentPlaylist.Click += new System.EventHandler(this.toolStripButtonDeleteCurrentPlaylist_Click);
            // 
            // toolStripButtonCheckFiles
            // 
            this.toolStripButtonCheckFiles.DisplayStyle = System.Windows.Forms.ToolStripItemDisplayStyle.Text;
            this.toolStripButtonCheckFiles.Image = ((System.Drawing.Image)(resources.GetObject("toolStripButtonCheckFiles.Image")));
            this.toolStripButtonCheckFiles.ImageTransparentColor = System.Drawing.Color.Magenta;
            this.toolStripButtonCheckFiles.Name = "toolStripButtonCheckFiles";
            this.toolStripButtonCheckFiles.Size = new System.Drawing.Size(48, 22);
            this.toolStripButtonCheckFiles.Text = "update";
            this.toolStripButtonCheckFiles.Click += new System.EventHandler(this.toolStripButtonCheckFiles_Click);
            // 
            // buttonExit
            // 
            this.buttonExit.Location = new System.Drawing.Point(405, 12);
            this.buttonExit.Name = "buttonExit";
            this.buttonExit.Size = new System.Drawing.Size(56, 23);
            this.buttonExit.TabIndex = 21;
            this.buttonExit.Text = "exit";
            this.buttonExit.UseVisualStyleBackColor = true;
            this.buttonExit.Click += new System.EventHandler(this.buttonExit_Click);
            // 
            // labelFile
            // 
            this.labelFile.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.labelFile.Location = new System.Drawing.Point(62, 72);
            this.labelFile.Name = "labelFile";
            this.labelFile.Size = new System.Drawing.Size(399, 18);
            this.labelFile.TabIndex = 23;
            this.labelFile.Text = "no file selected";
            // 
            // MainForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(473, 491);
            this.Controls.Add(this.labelFile);
            this.Controls.Add(label4);
            this.Controls.Add(this.buttonExit);
            this.Controls.Add(this.toolStrip2);
            this.Controls.Add(this.comboBoxPlaylists);
            this.Controls.Add(label3);
            this.Controls.Add(this.treeViewPlaylistEntries);
            this.Controls.Add(this.buttonPause);
            this.Controls.Add(this.buttonStop);
            this.Controls.Add(this.buttonPrev);
            this.Controls.Add(this.buttonNext);
            this.Controls.Add(this.buttonPlay);
            this.Controls.Add(label2);
            this.Controls.Add(this.labelFolder);
            this.Controls.Add(label1);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MinimumSize = new System.Drawing.Size(489, 39);
            this.Name = "MainForm";
            this.Text = "Medienverwaltung.Playlist";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.MainForm_FormClosing);
            this.FormClosed += new System.Windows.Forms.FormClosedEventHandler(this.MainForm_FormClosed);
            this.Load += new System.EventHandler(this.MainForm_Load);
            this.contextMenuStrip1.ResumeLayout(false);
            this.toolStrip2.ResumeLayout(false);
            this.toolStrip2.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.NotifyIcon notifyIcon1;
        private System.Windows.Forms.ContextMenuStrip contextMenuStrip1;
        private System.Windows.Forms.ToolStripMenuItem pauseToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem stopToolStripMenuItem;
        private System.Windows.Forms.ToolStripMenuItem prevToolStripMenuItem;
        private System.Windows.Forms.FolderBrowserDialog folderBrowserDialog1;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.ToolStripMenuItem exitToolStripMenuItem;
        private System.Windows.Forms.Label labelFolder;
        private System.Windows.Forms.Button buttonPlay;
        private System.Windows.Forms.Button buttonNext;
        private System.Windows.Forms.Button buttonPrev;
        private System.Windows.Forms.Button buttonStop;
        private System.Windows.Forms.Button buttonPause;
        private System.Windows.Forms.TreeView treeViewPlaylistEntries;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem1;
        private System.Windows.Forms.ToolStripMenuItem toolStripMenuItem2;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.ComboBox comboBoxPlaylists;
        private System.Windows.Forms.ToolStrip toolStrip2;
        private System.Windows.Forms.ToolStripButton toolStripButtonImportFromFolder;
        private System.Windows.Forms.ToolStripButton toolStripButtonDeleteCurrentPlaylist;
        private System.Windows.Forms.Button buttonExit;
        private System.Windows.Forms.ToolStripButton toolStripButtonCheckFiles;
        private System.Windows.Forms.Label labelFile;
    }
}

