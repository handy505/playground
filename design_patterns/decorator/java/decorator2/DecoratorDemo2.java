// Use Composition

class A{
    private String message;

    A(){
        message = "DecoratorDemo";
    } 

    public String get_message(){
        return message;
    }
}

class B{
    private A origin;

    B(A a){
        origin = a;
    }
    
    public String get_message(){
        return "<b>" + origin.get_message() + "</b>";
    }

}

public class DecoratorDemo2{
    public static void main(String[] args){

        A a = new A();
        B b = new B(a);

        System.out.println(a.get_message());
        System.out.println(b.get_message());

    }
}

/*
handy@ubuntu:~/demo/design_patterns/decorator/java/decorator2$ java DecoratorDemo2 
DecoratorDemo
<b>DecoratorDemo</b>
*/
