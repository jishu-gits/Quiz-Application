import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import java.awt.event.*;
import java.awt.*;

public class Rules extends JFrame implements ActionListener{
    static String name;
    JButton back,start;
    
    Rules(String name){
        Rules.name = name;
        getContentPane().setBackground(Color.WHITE);
        setLayout(null);

        JLabel heading = new JLabel("Welcome " + name + " JETSO TEST");
        heading.setBounds(50, 20, 700, 30);
        heading.setFont(new Font("Viner Hand ITC", Font.BOLD, 40));
        heading.setForeground(new Color(30, 144, 254));
        add(heading);

        JLabel rules = new JLabel();
        rules.setBounds(20, 90, 700, 350);
        rules.setFont(new Font("Tahoma", Font.PLAIN, 16));
        rules.setForeground(Color.BLACK);
        rules.setText("<html>"
        + "1. You have a limited time to answer each question.<br><br>"
        + "2. Each question has four options; only one is correct.<br><br>"
        + "3. No negative marking for incorrect answers.<br><br>"
        + "4. Once an answer is selected, it cannot be changed.<br><br>"
        + "5. Try to answer all questions before the timer runs out.<br><br>"
        + "6. Your final score will be displayed at the end.<br>"
        + "</html>"
        );
        add(rules);

        start = new JButton("Start");
        start.setBounds(250, 500, 100, 30);
        start.setBackground(new Color(30, 144, 254));
        start.setForeground(Color.WHITE);
        start.addActionListener(this);
        add(start);

        back = new JButton("Back");
        back.setBounds(400, 500, 100, 30);
        back.setBackground(new Color(30, 144, 254));
        back.setForeground(Color.WHITE);
        back.addActionListener(this);
        add(back);

        setSize(800, 650);
        setLocation(350, 100);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }

    public void actionPerformed(ActionEvent ae){
        if (ae.getSource() == start){
            setVisible(false);
            try {
                // Try to start the Quiz
                new Quiz(name);
            } catch (Exception e) {
                // If Quiz class doesn't exist, show an error message
                JOptionPane.showMessageDialog(this, 
                    "Quiz class not found or error occurred.\nPlease ensure Quiz.java is compiled and available.", 
                    "Error", 
                    JOptionPane.ERROR_MESSAGE);
                setVisible(true); // Show this window again
                System.out.println("Error starting quiz: " + e.getMessage());
            }
        } else {
            setVisible(false);
            try {
                new Login();
            } catch (Exception e) {
                // If Login class doesn't exist, show an error message
                JOptionPane.showMessageDialog(this, 
                    "Login class not found or error occurred.\nPlease ensure Login.java is compiled and available.", 
                    "Error", 
                    JOptionPane.ERROR_MESSAGE);
                System.out.println("Error opening login: " + e.getMessage());
                System.exit(0); // Exit if we can't go back to login
            }
        }
    }
    
    public static void main(String[] args){
        new Rules("User");
    }
}