using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AutoForm
{
    public partial class Form1 : Form
    {
        private static readonly HttpClient client = new HttpClient();

        public Form1()
        {
            InitializeComponent();
            InitializeDragDrop();
            AddTestButton();
            client.BaseAddress = new Uri("http://localhost:8000");
        }
         
        private void AddTestButton()
        {
            Button testBtn = new Button();
            testBtn.Text = "Test Drag-Drop";
            testBtn.Location = new Point(420, 350);
            testBtn.Click += (s, e) => {
                OpenFileDialog dialog = new OpenFileDialog();
                dialog.Filter = "Image Files|*.jpg;*.jpeg;*.png;*.bmp";
                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    pictureBoxForm.ImageLocation = dialog.FileName;
                    ProcessImageWithApiAsync(dialog.FileName);
                }
            };
            this.Controls.Add(testBtn);
        }
        private void InitializeDragDrop()
        {
            this.AllowDrop = true;
            this.DragEnter += new DragEventHandler(Form1_DragEnter);
            this.DragDrop += new DragEventHandler(Form1_DragDrop);
        }

        private void Form1_DragEnter(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                e.Effect = DragDropEffects.Copy;
            }
            else
            {
                e.Effect = DragDropEffects.None;
            }
        }

        private async void Form1_DragDrop(object sender, DragEventArgs e)
        {
            string[] files = (string[])e.Data.GetData(DataFormats.FileDrop);
            if (files != null && files.Any())
            {
                string filePath = files[0];
                string extension = Path.GetExtension(filePath).ToLowerInvariant();
                string[] validExtensions = { ".jpg", ".jpeg", ".png", ".bmp" };
                if (!validExtensions.Contains(extension))
                {
                    MessageBox.Show("Please drop a valid image file (JPG, PNG, BMP).", "Invalid File Type", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    return;
                }
                pictureBoxForm.ImageLocation = filePath;
                await ProcessImageWithApiAsync(filePath);
            }
        }

        private async Task ProcessImageWithApiAsync(string imagePath)
        {
            if (string.IsNullOrEmpty(imagePath) || !File.Exists(imagePath))
            {
                MessageBox.Show("The image file is invalid or does not exist.", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            try
            {
                this.Text = "Extractor - Processing, please wait...";
                this.Cursor = Cursors.WaitCursor;
                using (var multipartFormContent = new MultipartFormDataContent())
                {
                    byte[] fileBytes = File.ReadAllBytes(imagePath);
                    var fileContent = new ByteArrayContent(fileBytes);
                    multipartFormContent.Add(fileContent, "file", Path.GetFileName(imagePath));
                    var response = await client.PostAsync("/extract-form/", multipartFormContent);
                    response.EnsureSuccessStatusCode();
                    string jsonResponse = await response.Content.ReadAsStringAsync();

                     
                    MessageBox.Show($"API Response: {jsonResponse}", "Debug", MessageBoxButtons.OK, MessageBoxIcon.Information);

                    var extractedData = JsonConvert.DeserializeObject<Dictionary<string, string>>(jsonResponse);
                    PopulateFormFields(extractedData);
                    MessageBox.Show("Extraction complete!", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (HttpRequestException httpEx)
            {
                MessageBox.Show($"Could not connect to the AI service. Please ensure the Python API is running.\n\nDetails: {httpEx.Message}", "API Connection Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"An unexpected error occurred: {ex.Message}", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                this.Text = "Universal Info Extractor";
                this.Cursor = Cursors.Default;
            }
        }

        private void PopulateFormFields(Dictionary<string, string> data)
        {
            
            txtFirstName.Clear();
            txtLastName.Clear();
            txtMajor.Clear();
            txtGpa.Clear();

            // 2. Safely check for each key. If a key doesn't exist, the textbox remains empty.
            // This prevents the application from crashing.
            if (data.TryGetValue("STUDENT_FIRST_NAME", out string firstName))
            {
                txtFirstName.Text = firstName; 
            }
            if (data.TryGetValue("STUDENT_LAST_NAME", out string lastName))
            {
                txtLastName.Text = lastName;
            }
            if (data.TryGetValue("MAJOR", out string major))
            {
                txtMajor.Text = major;
            }
            if (data.TryGetValue("GPA", out string gpa))
            {
                txtGpa.Text = gpa;
            }
        }
    }
}