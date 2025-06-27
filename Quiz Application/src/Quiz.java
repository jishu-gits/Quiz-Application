import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.io.File;
import javax.imageio.ImageIO;
import javax.swing.*;
import java.net.http.*;
import java.net.URI;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Quiz extends JFrame implements ActionListener {

    // Arrays to store quiz data (initially declared with a placeholder capacity)
    String[][] questions;
    String[][] answers;
    String[][] useranswer;
    int questionCount = 0; // will be set after loading dynamic data
    
    JLabel qno, questionLabel;
    JRadioButton opt1, opt2, opt3, opt4;
    JButton next, submit;
    public static int timer = 15;
    public static int count = 0;
    public static int score = 0;
    ButtonGroup groupoptions;
    String name;
    private javax.swing.Timer swingTimer;
    
    public Quiz(String name) {
        this.name = name;
        setBounds(50, 0, 1440, 850);
        getContentPane().setBackground(Color.WHITE);
        setLayout(null);

        // Background image (upper half)
        try {
            File file = new File("C:\\Official Store\\Codes\\Java\\Quiz Application\\quiz.jpg");
            BufferedImage image = ImageIO.read(file);
            Image resizedImage = image.getScaledInstance(1440, 720, Image.SCALE_SMOOTH);
            ImageIcon resizedIcon = new ImageIcon(resizedImage);
            JLabel imageLabel = new JLabel(resizedIcon);
            imageLabel.setBounds(0, 0, 1440, 425);
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
        
        // Load quiz questions from the Python service
        loadQuizQuestions();
        
        // Create radio buttons for options
        opt1 = new JRadioButton();
        opt1.setBounds(170, 520, 700, 30);
        opt1.setBackground(Color.WHITE);
        opt1.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt1);
        
        opt2 = new JRadioButton();
        opt2.setBounds(170, 560, 700, 30);
        opt2.setBackground(Color.WHITE);
        opt2.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt2);
        
        opt3 = new JRadioButton();
        opt3.setBounds(170, 600, 700, 30);
        opt3.setBackground(Color.WHITE);
        opt3.setFont(new Font("Dialog", Font.PLAIN, 20));
        add(opt3);
        
        opt4 = new JRadioButton();
        opt4.setBounds(170, 640, 700, 30);
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
        next.setForeground(Color.WHITE);
        next.addActionListener(this);
        add(next);
        
        submit = new JButton("Submit");
        submit.setBounds(1100, 710, 200, 40);
        submit.setFont(new Font("Tahoma", Font.PLAIN, 22));
        submit.setBackground(new Color(30, 144, 255));
        submit.setForeground(Color.WHITE);
        submit.setEnabled(false);
        submit.addActionListener(this);
        add(submit);
        
        // Start the quiz if questions were loaded
        if (questionCount > 0) {
            start(count);
        } else {
            JOptionPane.showMessageDialog(this, "No quiz questions available");
        }
        
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }
    
    // Loads quiz questions by calling the Python service and parsing the JSON
    private void loadQuizQuestions() {
        try {
            HttpClient client = HttpClient.newHttpClient();
            // Endpoint exposed by your Python service that returns quiz questions in JSON format
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:5000/extractQuestions"))
                    .build();
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() == 200) {
                ObjectMapper mapper = new ObjectMapper();
                JsonNode root = mapper.readTree(response.body());
                JsonNode questionsArray = root.get("questions");
                questionCount = questionsArray.size();
                // Resize arrays to the number of loaded questions
                questions = new String[questionCount][5];
                answers = new String[questionCount][1];
                useranswer = new String[questionCount][1];
                int index = 0;
                for (JsonNode q: questionsArray){
                    if (q.get("question") != null){
                        questions[index][0] = q.get("question").asText();
                    }else{
                        questions[index][0] = "";
                    }
                    
                    JsonNode opts = q.get("options");

                    if (opts != null && opts.isArray()){
                        for (int i = 0; i<4; i++){
                            if (i < opts.size() && opts.get(i) != null){
                                questions[index][i+ 1] = opts.get(i).asText();
                            }else{
                                questions[index][i + 1] = "";
                            }
                        }
                    }else{
                        questions[index][1] = "";
                        questions[index][2] = "";
                        questions[index][3] = "";
                        questions[index][4] = "";
                    }
                    if(q.get("answer") != null){
                        answers[index][0] = q.get("answer").asText();
                    }else{
                        answers[index][0] = "";
                    }
                    index++;
                    if (index >= questions.length) break;
                }
            } else {
                JOptionPane.showMessageDialog(this, "Error loading quiz questions:\n" + response.body());
            }
        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showMessageDialog(this, "Exception loading quiz questions:\n" + e.getMessage());
        }
    }
    
    public void actionPerformed(ActionEvent ae) {
        if (ae.getSource() == next) {
            if (swingTimer != null) {
                swingTimer.stop();
            }
            // Save current answer (if any)
            if (groupoptions.getSelection() != null) {
                useranswer[count][0] = groupoptions.getSelection().getActionCommand();
            } else {
                useranswer[count][0] = "";
            }
            count++;
            if (count == questionCount - 1) {
                next.setEnabled(false);
                submit.setEnabled(true);
            }
            start(count);
        } else if (ae.getSource() == submit) {
            if (swingTimer != null) {
                swingTimer.stop();
            }
            // Save final answer
            if (groupoptions.getSelection() != null) {
                useranswer[count][0] = groupoptions.getSelection().getActionCommand();
            } else {
                useranswer[count][0] = "";
            }
            calculateAndShowScore();
        }
    }
    
    public void paint(Graphics g) {
        super.paint(g);
        String time = "Time Left " + timer + " seconds";
        g.setColor(Color.RED);
        g.setFont(new Font("Tahoma", Font.BOLD, 25));
        if (timer > 0) {
            g.drawString(time, 1100, 500);
        } else {
            g.drawString("Time's up!!", 1100, 500);
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
        if (groupoptions.getSelection() != null) {
            useranswer[count][0] = groupoptions.getSelection().getActionCommand();
        } else {
            useranswer[count][0] = "";
        }
        if (count == questionCount - 1) {
            calculateAndShowScore();
        } else {
            count++;
            if (count == questionCount - 1) {
                next.setEnabled(false);
                submit.setEnabled(true);
            }
            start(count);
        }
    }
    
    private void calculateAndShowScore() {
        score = 0;
        for (int i = 0; i < questionCount; i++) {
            if (useranswer[i][0] != null && useranswer[i][0].equals(answers[i][0])) {
                score += 10;
            }
        }
        setVisible(false);
        new Score(name, score);
    }
    
    public void start(int Count) {
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
        startTimer();
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
        
        JLabel heading = new JLabel("Quiz Results");
        heading.setBounds(280, 30, 300, 30);
        heading.setFont(new Font("Tahoma", Font.BOLD, 32));
        heading.setForeground(new Color(30, 144, 255));
        add(heading);
        
        JLabel nameLabel = new JLabel("Name: " + name);
        nameLabel.setBounds(50, 120, 300, 30);
        nameLabel.setFont(new Font("Tahoma", Font.PLAIN, 26));
        add(nameLabel);
        
        
        JLabel scoreLabel = new JLabel("Your Score: " + score + " out of " + ("100"));
        scoreLabel.setBounds(50, 180, 400, 30);
        scoreLabel.setFont(new Font("Tahoma", Font.PLAIN, 26));
        add(scoreLabel);
        
        String performance;
        if (score >= 80) {
            performance = "Excellent! Well done!";
        } else if (score >= 60) {
            performance = "Good job! Keep it up!";
        } else if (score >= 50) {
            performance = "Not bad, but you can do better!";
        } else {
            performance = "Better luck next time!";
        }
        
        JLabel performanceLabel = new JLabel(performance);
        performanceLabel.setBounds(50, 240, 400, 30);
        performanceLabel.setFont(new Font("Tahoma", Font.PLAIN, 20));
        performanceLabel.setForeground(new Color(255, 69, 0));
        add(performanceLabel);
        
        restart = new JButton("Restart Quiz");
        restart.setBounds(50, 350, 200, 40);
        restart.setFont(new Font("Tahoma", Font.PLAIN, 18));
        restart.setBackground(new Color(30, 144, 255));
        restart.setForeground(Color.WHITE);
        restart.addActionListener(this);
        add(restart);
        
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
            Quiz.timer = 15;
            Quiz.count = 0;
            Quiz.score = 0;
            new Quiz(name);
        } else if (ae.getSource() == exit) {
            System.exit(0);
        }
    }
}
