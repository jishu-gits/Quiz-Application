import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.event.*;

public class Quiz extends JFrame implements ActionListener{

    String questions[][] = new String[10][5];
    String answers[][] = new String [10][2];
    String useranswer[][] = new String [10][1];
    JLabel qno, questionLabel;
    JRadioButton opt1, opt2, opt3, opt4;
    JButton next, submit;
    public static int timer = 15;
    public static int count = 0;
    public static int score = 0;
    ButtonGroup groupoptions;
    String name;

    Quiz(String name) {
        this.name = name;
        setBounds(50, 0, 1440, 850); // Set frame size
        getContentPane().setBackground(Color.WHITE);
        setLayout(null); // Needed for absolute positioning

        try {
            // Load original image
            File file = new File("C:\\Official Store\\Codes\\Java\\Quiz Application\\quiz.jpg");
            BufferedImage image = ImageIO.read(file);

            // Scale image proportionally to fit top half (keeping aspect ratio)
            Image resizedImage = image.getScaledInstance(1440, 720, Image.SCALE_SMOOTH);
            ImageIcon resizedIcon = new ImageIcon(resizedImage);

            // Set up label (placing in top half, centered)
            JLabel imageLabel = new JLabel(resizedIcon);
            imageLabel.setBounds(0, 0, 1440, 425); // Adjusted bounds for top half
            add(imageLabel);

        } catch (Exception e) {
            e.printStackTrace();
        }

        qno = new JLabel();
        qno.setBounds(100, 450, 50, 30);
        qno.setFont(new Font("Tahoma", Font.PLAIN, 25));
        add(qno);
        
        questionLabel = new JLabel();
        questionLabel.setBounds(150, 450, 900, 30);
        questionLabel.setFont(new Font("Tahoma", Font.PLAIN, 25));
        add(questionLabel);

        questions[0][0] = "Which is used to find and fix bugs in the Java programs.?";
        questions[0][1] = "JVM";
        questions[0][2] = "JDB";
        questions[0][3] = "JDK";
        questions[0][4] = "JRE";

        questions[1][0] = "What is the return type of the hashCode() method in the Object class?";
        questions[1][1] = "int";
        questions[1][2] = "Object";
        questions[1][3] = "long";
        questions[1][4] = "void";

        questions[2][0] = "Which package contains the Random class?";
        questions[2][1] = "java.util package";
        questions[2][2] = "java.lang package";
        questions[2][3] = "java.awt package";
        questions[2][4] = "java.io package";

        questions[3][0] = "An interface with no fields or methods is known as?";
        questions[3][1] = "Runnable Interface";
        questions[3][2] = "Abstract Interface";
        questions[3][3] = "Marker Interface";
        questions[3][4] = "CharSequence Interface";

        questions[4][0] = "In which memory a String is stored, when we create a string using new operator?";
        questions[4][1] = "Stack";
        questions[4][2] = "String memory";
        questions[4][3] = "Random storage space";
        questions[4][4] = "Heap memory";

        questions[5][0] = "Which of the following is a marker interface?";
        questions[5][1] = "Runnable interface";
        questions[5][2] = "Remote interface";
        questions[5][3] = "Readable interface";
        questions[5][4] = "Result interface";

        questions[6][0] = "Which keyword is used for accessing the features of a package?";
        questions[6][1] = "import";
        questions[6][2] = "package";
        questions[6][3] = "extends";
        questions[6][4] = "export";

        questions[7][0] = "In java, jar stands for?";
        questions[7][1] = "Java Archive Runner";
        questions[7][2] = "Java Archive";
        questions[7][3] = "Java Application Resource";
        questions[7][4] = "Java Application Runner";

        questions[8][0] = "Which of the following is a mutable class in java?";
        questions[8][1] = "java.lang.StringBuilder";
        questions[8][2] = "java.lang.Short";
        questions[8][3] = "java.lang.Byte";
        questions[8][4] = "java.lang.String";

        questions[9][0] = "Which of the following option leads to the portability and security of Java?";
        questions[9][1] = "Bytecode is executed by JVM";
        questions[9][2] = "The applet makes the Java code secure and portable";
        questions[9][3] = "Use of exception handling";
        questions[9][4] = "Dynamic binding between objects";

        answers[0][1] = "JDB";
        answers[1][1] = "int";
        answers[2][1] = "java.util package";
        answers[3][1] = "Marker Interface";
        answers[4][1] = "Heap memory";
        answers[5][1] = "Remote interface";
        answers[6][1] = "import";
        answers[7][1] = "Java Archive";
        answers[8][1] = "java.lang.StringBuilder";
        answers[9][1] = "Bytecode is executed by JVM";

        opt1 = new JRadioButton();
        opt1.setBounds(170,520,700,30);
        opt1.setBackground(Color.WHITE);
        opt1.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt1);

        opt2 = new JRadioButton();
        opt2.setBounds(170,560,700,30);
        opt2.setBackground(Color.WHITE);
        opt2.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt2);

        opt3 = new JRadioButton();
        opt3.setBounds(170,600,700,30);
        opt3.setBackground(Color.WHITE);
        opt3.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt3);

        opt4 = new JRadioButton();
        opt4.setBounds(170,640,700,30);
        opt4.setBackground(Color.WHITE);
        opt4.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt4);

        groupoptions = new ButtonGroup();
        groupoptions.add(opt1);
        groupoptions.add(opt2);
        groupoptions.add(opt3);
        groupoptions.add(opt4);

        next = new JButton("Next");
        next.setBounds(1100, 630, 200, 40);
        next.setFont(new Font("Tahoma", Font.PLAIN, 22));
        next.setBackground(new Color(30, 144, 255));
        next.setForeground(Color.white);
        next.addActionListener(this);
        add(next);

        submit = new JButton("Submit");
        submit.setBounds(1100, 710, 200, 40);
        submit.setFont(new Font("Tahoma", Font.PLAIN, 22));
        submit.setBackground(new Color(30, 144, 255));
        submit.setForeground(Color.white);
        submit.setEnabled(false);
        submit.addActionListener(this);
        add(submit);

        start(count);

        setVisible(true);
    }

    public void actionPerformed(ActionEvent ae){
        if (ae.getSource() == next){
            // Stop current timer
            if (swingTimer != null) {
                swingTimer.stop();
            }
            
            // Store current answer
            if (groupoptions.getSelection() != null) {
                useranswer[count][0] = groupoptions.getSelection().getActionCommand();
            } else {
                useranswer[count][0] = "";
            }            
            
            count++;
            if(count == 9){
                next.setEnabled(false);
                submit.setEnabled(true);
            }
            start(count);
        }else if(ae.getSource() == submit){
            // Stop current timer
            if (swingTimer != null) {
                swingTimer.stop();
            }
            
            // Store final answer
            if (groupoptions.getSelection() != null) {
                useranswer[count][0] = groupoptions.getSelection().getActionCommand();
            } else {
                useranswer[count][0] = "";
            }
            
            calculateAndShowScore();
        }
    }

    private javax.swing.Timer swingTimer;
    
    public void paint(Graphics g){
        super.paint(g);
        String time = "Time Left " + timer + " seconds";
        g.setColor(Color.RED);
        g.setFont(new Font("Tahoma", Font.BOLD, 25));

        if (timer > 0) {
            g.drawString(time, 1100, 500);
        } else {
            g.drawString("Times up!! ", 1100, 500);
        }
    }
    
    public void startTimer() {
        timer = 15;
        if (swingTimer != null) {
            swingTimer.stop();
        }
        
        swingTimer = new javax.swing.Timer(1000, new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                timer--;
                repaint();
                
                if (timer < 0) {
                    swingTimer.stop();
                    timeUp();
                }
            }
        });
        swingTimer.start();
    }
    
    private void timeUp() {
        // Store current answer if any
        if (groupoptions.getSelection() != null) {
            useranswer[count][0] = groupoptions.getSelection().getActionCommand();
        } else {
            useranswer[count][0] = "";
        }
        
        if (count == 9) {
            // Last question - calculate score and show results
            calculateAndShowScore();
        } else {
            // Move to next question
            count++;
            if (count == 9) {
                next.setEnabled(false);
                submit.setEnabled(true);
            }
            start(count);
        }
    }
    
    private void calculateAndShowScore() {
        for (int i = 0; i < useranswer.length; i++) {
            if (useranswer[i][0] != null && useranswer[i][0].equals(answers[i][1])) {
                score += 10;
            }
        }
        setVisible(false);
        new Score(name, score);
    }

    public void start(int Count){
        qno.setText("" + (Count + 1) + ".");
        questionLabel.setText(questions[Count][0]);
        opt1.setText(questions[Count][1]);
        opt1.setActionCommand(questions[Count][1]);
        opt2.setText(questions[Count][2]);
        opt2.setActionCommand(questions[Count][2]);
        opt3.setText(questions[Count][3]);
        opt3.setActionCommand(questions[Count][3]);
        opt4.setText(questions[Count][4]);
        opt4.setActionCommand(questions[Count][4]);

        groupoptions.clearSelection();
        startTimer(); // Start the timer for this question
    }

    public static void main(String[] args) {
        new Quiz("User");
    }
}

// Score class to display quiz results
class Score extends JFrame implements ActionListener {
    String name;
    int score;
    JButton restart, exit;
    
    Score(String name, int score) {
        this.name = name;
        this.score = score;
        
        setBounds(400, 150, 750, 550);
        getContentPane().setBackground(Color.WHITE);
        setLayout(null);
        
        // Title
        JLabel heading = new JLabel("Quiz Results");
        heading.setBounds(280, 30, 300, 30);
        heading.setFont(new Font("Tahoma", Font.BOLD, 32));
        heading.setForeground(new Color(30, 144, 255));
        add(heading);
        
        // Name display
        JLabel nameLabel = new JLabel("Name: " + name);
        nameLabel.setBounds(50, 120, 300, 30);
        nameLabel.setFont(new Font("Tahoma", Font.PLAIN, 26));
        add(nameLabel);
        
        // Score display
        JLabel scoreLabel = new JLabel("Your Score: " + score + " out of 100");
        scoreLabel.setBounds(50, 180, 400, 30);
        scoreLabel.setFont(new Font("Tahoma", Font.PLAIN, 26));
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
        
        JLabel performanceLabel = new JLabel(performance);
        performanceLabel.setBounds(50, 240, 400, 30);
        performanceLabel.setFont(new Font("Tahoma", Font.PLAIN, 20));
        performanceLabel.setForeground(new Color(255, 69, 0));
        add(performanceLabel);
        
        // Restart button
        restart = new JButton("Restart Quiz");
        restart.setBounds(50, 350, 200, 40);
        restart.setFont(new Font("Tahoma", Font.PLAIN, 18));
        restart.setBackground(new Color(30, 144, 255));
        restart.setForeground(Color.WHITE);
        restart.addActionListener(this);
        add(restart);
        
        // Exit button
        exit = new JButton("Exit");
        exit.setBounds(300, 350, 200, 40);
        exit.setFont(new Font("Tahoma", Font.PLAIN, 18));
        exit.setBackground(new Color(255, 69, 0));
        exit.setForeground(Color.WHITE);
        exit.addActionListener(this);
        add(exit);
        
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setVisible(true);
    }
    
    public void actionPerformed(ActionEvent ae) {
        if (ae.getSource() == restart) {
            setVisible(false);
            // Reset static variables
            Quiz.timer = 15;
            Quiz.count = 0;
            Quiz.score = 0;
            new Quiz(name);
        } else if (ae.getSource() == exit) {
            System.exit(0);
        }
    }
}