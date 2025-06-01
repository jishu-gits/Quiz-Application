import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.event.*;

public class Score extends JFrame implements ActionListener, ComponentListener {
    String name;
    int score;
    JButton restart, exit;
    JLabel imageLabel, heading, nameLabel, scoreLabel, performanceLabel;
    
    Score(String name, int score) {
        this.name = name;
        this.score = score;
        
        // Get screen dimensions for better initial sizing
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int width = Math.min(800, (int)(screenSize.width * 0.6));
        int height = Math.min(600, (int)(screenSize.height * 0.7));
        
        setBounds((screenSize.width - width) / 2, (screenSize.height - height) / 2, width, height);
        setMinimumSize(new Dimension(600, 450));
        getContentPane().setBackground(Color.WHITE);
        setLayout(null);
        
        // Add component listener for resize events
        addComponentListener(this);

        // Initialize components
        initializeComponents();
        
        // Initial layout
        layoutComponents();
        
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }
    
    private void initializeComponents() {
        // Background image
        imageLabel = new JLabel();
        loadBackgroundImage();
        add(imageLabel);

        // Title
        heading = new JLabel("Quiz Results", SwingConstants.CENTER);
        heading.setFont(new Font("Tahoma", Font.BOLD, 32));
        heading.setForeground(new Color(30, 144, 255));
        add(heading);
        
        // Name display
        nameLabel = new JLabel("Name: " + name);
        nameLabel.setFont(new Font("Tahoma", Font.PLAIN, 24));
        add(nameLabel);
        
        // Score display
        scoreLabel = new JLabel("Your Score: " + score + " out of 100");
        scoreLabel.setFont(new Font("Tahoma", Font.PLAIN, 24));
        add(scoreLabel);
        
        // Performance message
        String performance;
        if (score >= 80) {
            performance = "Excellent! Well done!";
        } else if (score >= 60) {
            performance = "Good job! Keep it up!";
        } else if (score >= 40) {
            performance = "Not bad, but you can do better!";
        } else {
            performance = "Better luck next time!";
        }
        
        performanceLabel = new JLabel(performance);
        performanceLabel.setFont(new Font("Tahoma", Font.PLAIN, 18));
        performanceLabel.setForeground(new Color(255, 69, 0));
        add(performanceLabel);
        
        // Restart button
        restart = new JButton("Play Again");
        restart.setFont(new Font("Tahoma", Font.PLAIN, 16));
        restart.setBackground(new Color(30, 144, 255));
        restart.setForeground(Color.WHITE);
        restart.addActionListener(this);
        restart.setFocusPainted(false);
        restart.setBorderPainted(false);
        add(restart);
        
        // Exit button
        exit = new JButton("Exit");
        exit.setFont(new Font("Tahoma", Font.PLAIN, 16));
        exit.setBackground(new Color(255, 69, 0));
        exit.setForeground(Color.WHITE);
        exit.addActionListener(this);
        exit.setFocusPainted(false);
        exit.setBorderPainted(false);
        add(exit);
    }
    
    private void loadBackgroundImage() {
        try {
            File file = new File("score.jpg");
            BufferedImage image = ImageIO.read(file);
            
            // Scale image based on current window size
            int width = getWidth();
            int height = (int)(getHeight() * 0.4); // Use 40% of window height for image
            
            Image resizedImage = image.getScaledInstance(width, height, Image.SCALE_SMOOTH);
            ImageIcon resizedIcon = new ImageIcon(resizedImage);
            imageLabel.setIcon(resizedIcon);

        } catch (Exception e) {
            // If image not found, create a colored background panel
            imageLabel.setOpaque(true);
            imageLabel.setBackground(new Color(240, 248, 255));
            System.out.println("Background image not found, using colored background.");
        }
    }
    
    private void layoutComponents() {
        int windowWidth = getWidth();
        int windowHeight = getHeight();
        
        // Calculate responsive dimensions
        int margin = windowWidth / 20; // 5% margin
        int imageHeight = (int)(windowHeight * 0.35);
        int contentStartY = imageHeight + 20;
        int buttonWidth = Math.min(150, windowWidth / 6);
        int buttonHeight = 40;
        
        // Background image
        imageLabel.setBounds(0, 0, windowWidth, imageHeight);
        
        // Title - centered
        heading.setBounds(margin, contentStartY, windowWidth - (2 * margin), 40);
        
        // Name label
        nameLabel.setBounds(margin, contentStartY + 60, windowWidth - (2 * margin), 30);
        
        // Score label
        scoreLabel.setBounds(margin, contentStartY + 100, windowWidth - (2 * margin), 30);
        
        // Performance label
        performanceLabel.setBounds(margin, contentStartY + 140, windowWidth - (2 * margin), 30);
        
        // Buttons - centered horizontally
        int buttonY = contentStartY + 190;
        int totalButtonWidth = (2 * buttonWidth) + 20; // 20px gap between buttons
        int buttonStartX = (windowWidth - totalButtonWidth) / 2;
        
        restart.setBounds(buttonStartX, buttonY, buttonWidth, buttonHeight);
        exit.setBounds(buttonStartX + buttonWidth + 20, buttonY, buttonWidth, buttonHeight);
        
        // Adjust font sizes based on window size
        adjustFontSizes();
    }
    
    private void adjustFontSizes() {
        int windowWidth = getWidth();
        
        // Scale fonts based on window width
        int titleSize = Math.max(20, Math.min(36, windowWidth / 25));
        int textSize = Math.max(16, Math.min(26, windowWidth / 35));
        int buttonSize = Math.max(12, Math.min(18, windowWidth / 50));
        int performanceSize = Math.max(14, Math.min(20, windowWidth / 45));
        
        heading.setFont(new Font("Tahoma", Font.BOLD, titleSize));
        nameLabel.setFont(new Font("Tahoma", Font.PLAIN, textSize));
        scoreLabel.setFont(new Font("Tahoma", Font.PLAIN, textSize));
        performanceLabel.setFont(new Font("Tahoma", Font.PLAIN, performanceSize));
        restart.setFont(new Font("Tahoma", Font.PLAIN, buttonSize));
        exit.setFont(new Font("Tahoma", Font.PLAIN, buttonSize));
    }
    
    // ComponentListener methods for handling window resize
    @Override
    public void componentResized(ComponentEvent e) {
        loadBackgroundImage(); // Reload image with new size
        layoutComponents();    // Recalculate layout
        repaint();            // Refresh display
    }
    
    @Override
    public void componentMoved(ComponentEvent e) {}
    
    @Override
    public void componentShown(ComponentEvent e) {}
    
    @Override
    public void componentHidden(ComponentEvent e) {}
    
    public void actionPerformed(ActionEvent ae) {
        if (ae.getSource() == restart) {
            setVisible(false);
            // Reset static variables in Quiz class
            Quiz.timer = 15;
            Quiz.count = 0;
            Quiz.score = 0;
            new Quiz(name);
        } else if (ae.getSource() == exit) {
            System.exit(0);
        }
    }

    public static void main(String[] args) {
        new Score("Test User", 75);
    }
}