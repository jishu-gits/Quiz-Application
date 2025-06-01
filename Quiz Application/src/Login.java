import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.*;

public class Login extends JFrame implements ActionListener{
    JButton rules, back;
    JTextField tfname;
    Login() {
        // Set up the main frame (this)
        setSize(1200, 500);
        setLocation(200, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(null);
        getContentPane().setBackground(Color.WHITE);

        try {
            // Load original image
            File file = new File("login.jpg");
            BufferedImage image = ImageIO.read(file);

            // Scale image to fit left half (600x500)
            Image resizedImage = image.getScaledInstance(600, 500, Image.SCALE_SMOOTH);
            ImageIcon resizedIcon = new ImageIcon(resizedImage);

            // Set up label
            JLabel imageLabel = new JLabel(resizedIcon);
            imageLabel.setBounds(0, 0, 600, 500); // Cover left half completely
            add(imageLabel);
        } catch (Exception e) {
            e.printStackTrace();
        }

        // Heading label
        JLabel heading = new JLabel("JETSO TESTO");
        heading.setBounds(750, 60, 300, 45);
        heading.setFont(new Font("Viner Hand ITC", Font.BOLD, 40));
        heading.setForeground(new Color(30, 144, 254));
        add(heading);

        JLabel name = new JLabel("Enter Your Name");
        name.setBounds(810,150, 300, 20);
        name.setFont(new Font("Mongolian Baiti", Font.BOLD, 18));
        name.setForeground(new Color(30, 144, 254));
        add(name);

        tfname = new JTextField();
        tfname.setBounds(735, 200, 300, 25);
        tfname.setFont(new Font("Times New Roman", Font.BOLD, 20));
        add(tfname);

        rules =  new JButton("Rules");
        rules.setBounds(735, 270, 120, 25);
        rules.setBackground(new Color(30, 144, 254));
        rules.setForeground(Color.WHITE);
        rules.addActionListener(this);
        add(rules);

        back =  new JButton("Back");
        back.setBounds(915, 270, 120, 25);
        back.setBackground(new Color(30, 144, 254));
        back.setForeground(Color.WHITE);
        back.addActionListener(this);
        add(back);


        // Make the frame visible
        setVisible(true);
    }
    public void actionPerformed(ActionEvent ae){
        if (ae.getSource() == rules){
            String name = tfname.getText();
            setVisible(false);
            new Rules(name);

        }else if (ae.getSource() == back){
            setVisible(false);

        }

    }

    public static void main(String[] args) {
        new Login();
    }
}
