import java.util.Date;
import java.text.*;

public class Main{

    public static void main(String[] args){
        
        Date dt = new Date();
        System.out.println(dt);

        // format
        SimpleDateFormat ft = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        System.out.println(ft.format(dt));

    }

}

