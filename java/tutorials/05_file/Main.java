import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class Main{
    public static void main(String[] args){

        // read file
        try{
            File fd     = new File("README.md");
            Scanner fds = new Scanner(fd);
            while(fds.hasNextLine()){
                String data = fds.nextLine();
                System.out.println(data);
            }
            fds.close();

        }catch(FileNotFoundException err){
            System.out.println("error");
        }



        // write file
        try{
            FileWriter fd = new FileWriter("demo.txt");
            fd.write("this is demo string writed to file.\n");
            fd.close();
            System.out.println("write file success.");

        }catch(IOException err){
            System.out.println("error");
        }

    }
}
