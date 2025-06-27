import java.awt.*;
import java.awt.datatransfer.*;
import java.awt.dnd.*;
import java.awt.event.*;
import java.awt.image.*;
import java.io.File;
import java.net.URI;
import java.net.http.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import javax.imageio.ImageIO;
import javax.swing.*;

public class Login extends JFrame implements ActionListener {
    JButton rules, back;
    JTextField tfname;
    JPanel pdfDropPanel; // Panel for drag & drop feature
    
    public Login() {
        // Set up the main frame
        setSize(1200, 500);
        setLocation(200, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(null);
        getContentPane().setBackground(Color.WHITE);

        // Left-side image display
        try {
            File file = new File("login.jpg");
            BufferedImage image = ImageIO.read(file);
            Image resizedImage = image.getScaledInstance(600, 500, Image.SCALE_SMOOTH);
            ImageIcon resizedIcon = new ImageIcon(resizedImage);
            JLabel imageLabel = new JLabel(resizedIcon);
            imageLabel.setBounds(0, 0, 600, 500);
            add(imageLabel);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Heading and user name input area
        JLabel heading = new JLabel("JETSO TESTO");
        heading.setBounds(750, 60, 300, 45);
        heading.setFont(new Font("Viner Hand ITC", Font.BOLD, 40));
        heading.setForeground(new Color(30, 144, 254));
        add(heading);

        JLabel name = new JLabel("Enter Your Name");
        name.setBounds(810, 150, 300, 20);
        name.setFont(new Font("Mongolian Baiti", Font.BOLD, 18));
        name.setForeground(new Color(30, 144, 254));
        add(name);

        tfname = new JTextField();
        tfname.setBounds(735, 200, 300, 25);
        tfname.setFont(new Font("Times New Roman", Font.BOLD, 20));
        add(tfname);

        // "Rules" and "Back" buttons
        rules = new JButton("Rules");
        rules.setBounds(735, 250, 120, 25);
        rules.setBackground(new Color(30, 144, 254));
        rules.setForeground(Color.WHITE);
        rules.addActionListener(this);
        add(rules);

        back = new JButton("Back");
        back.setBounds(915, 250, 120, 25);
        back.setBackground(new Color(30, 144, 254));
        back.setForeground(Color.WHITE);
        back.addActionListener(this);
        add(back);

        // Drag & Drop PDF Panel
        pdfDropPanel = new JPanel();
        pdfDropPanel.setBounds(735, 300, 300, 100);
        pdfDropPanel.setBackground(Color.LIGHT_GRAY);
        pdfDropPanel.setBorder(BorderFactory.createLineBorder(Color.GRAY));
        pdfDropPanel.setLayout(new BorderLayout());
        JLabel dropLabel = new JLabel("Drag & Drop PDF here", SwingConstants.CENTER);
        dropLabel.setFont(new Font("Arial", Font.BOLD, 16));
        pdfDropPanel.add(dropLabel, BorderLayout.CENTER);
        add(pdfDropPanel);

        // Enable drag and drop on the panel
        new DropTarget(pdfDropPanel, new DropTargetAdapter() {
            @Override
            public void drop(DropTargetDropEvent dtde) {
                try {
                    dtde.acceptDrop(DnDConstants.ACTION_COPY);
                    Transferable transferable = dtde.getTransferable();
                    DataFlavor[] flavors = transferable.getTransferDataFlavors();
                    for (DataFlavor flavor : flavors) {
                        if (flavor.isFlavorJavaFileListType()) {
                            List<File> files = (List<File>) transferable.getTransferData(DataFlavor.javaFileListFlavor);
                            if (!files.isEmpty()) {
                                File file = files.get(0);
                                if (file.getName().toLowerCase().endsWith(".pdf")) {
                                    // Upload PDF to your Python service
                                    uploadPDFFile(file);
                                } else {
                                    JOptionPane.showMessageDialog(null, "Please drop a valid PDF file.");
                                }
                            }
                            break;
                        }
                    }
                    dtde.dropComplete(true);
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
        });

        setVisible(true);
    }

    public void actionPerformed(ActionEvent ae) {
        if (ae.getSource() == rules) {
            String name = tfname.getText();
            setVisible(false);
            new Rules(name); // Launch the Rules screen (assuming a Rules class exists)
        } else if (ae.getSource() == back) {
            setVisible(false);
        }
    }
    
    // Method to upload the PDF file to the Python service
    private void uploadPDFFile(File file) {
        try {
            HttpClient client = HttpClient.newHttpClient();
            String boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW";
            HttpRequest.BodyPublisher bodyPublisher = buildFileBodyPublisher(file, boundary);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5000/extract"))
                    .header("Content-Type", "multipart/form-data; boundary=" + boundary)
                    .POST(bodyPublisher)
                    .build();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() == 200) {
                JOptionPane.showMessageDialog(this, "PDF processed successfully!");
                // Optionally, store or pass the received quiz data to the next screen.
            } else {
                JOptionPane.showMessageDialog(this, "Error processing PDF:\n" + response.body());
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(this, "Exception: " + ex.getMessage());
        }
    }
    
    // Helper to build a multipart/form-data body with the PDF file
    private HttpRequest.BodyPublisher buildFileBodyPublisher(File file, String boundary) throws Exception {
        List<byte[]> byteArrays = new ArrayList<>();
        String LINE_SEPARATOR = "\r\n";
        
        // File part header
        String partHeader = "--" + boundary + LINE_SEPARATOR +
               "Content-Disposition: form-data; name=\"file\"; filename=\"" + file.getName() + "\"" + LINE_SEPARATOR +
               "Content-Type: application/pdf" + LINE_SEPARATOR + LINE_SEPARATOR;
        byteArrays.add(partHeader.getBytes(StandardCharsets.UTF_8));
        byteArrays.add(Files.readAllBytes(file.toPath()));
        byteArrays.add(LINE_SEPARATOR.getBytes(StandardCharsets.UTF_8));
        
        // End boundary marker
        String ending = "--" + boundary + "--" + LINE_SEPARATOR;
        byteArrays.add(ending.getBytes(StandardCharsets.UTF_8));
        return HttpRequest.BodyPublishers.ofByteArrays(byteArrays);
    }
    
    public static void main(String[] args) {
        new Login();
    }
}
