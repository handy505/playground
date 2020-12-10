// Use Inheritance
class A{
    private String message;

    A(){
        message = "DecoratorDemo";
    } 

    public String get_message(){
        return message;
    }
}

class B extends A{
    private A origin;

    B(A a){
        origin = a;
    }
    
    @Override
    public String get_message(){
        return "<b>" + origin.get_message() + "</b>";
    }

}

public class DecoratorDemo3{
    public static void main(String[] args){

        A a = new A();
        B b = new B(a);

        System.out.println(a.get_message());
        System.out.println(b.get_message());

    }
}

/*
handy@ubuntu:~/demo/design_patterns/decorator/java/decorator3$ java DecoratorDemo3
DecoratorDemo
<b>DecoratorDemo</b>
*/
