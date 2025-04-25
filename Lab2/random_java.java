import java.io.FileWriter;
import java.util.Random;

public class random_java {
    public static void main(String[] args) throws Exception {
        FileWriter file = new FileWriter("sequence_java.txt");
        Random rand = new Random();

        for (int i = 0; i < 128; ++i) {
            file.write(rand.nextInt(2) + "");
        }
        file.close();
    }
}