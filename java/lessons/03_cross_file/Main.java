//import mypackage.*;

public class Main{

    public static void main(String[] args){
        
        // without import statement
        int res = mypackage.MyClass.add(2,3);
        System.out.println("result = " + res);

        // use import statement
        //int res = MyClass.add(2,3);
        //System.out.println("result = " + res);
    }

}

