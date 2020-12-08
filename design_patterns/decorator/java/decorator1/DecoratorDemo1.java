
class A{
    private String message;

    A(){
        message = "DecoratorDemo";
    } 

    public String get_message(){
        return message;
    }
}

public class DecoratorDemo1{
    public static void main(String[] args){

        A a = new A();
        String msg = a.get_message();
        System.out.println(msg);

        String s = "<u>" + msg + "</u>";
        System.out.println(s);

        s = "<b>" + s + "</b>";
        System.out.println(s);
    }
}

