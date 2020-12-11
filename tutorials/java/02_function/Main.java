public class Main{
    public static void main(String[] args){
        int res = Operator.add(2,3);
        System.out.println("result = " + res);
    }
}

class Operator{
    public static int add(int a, int b){
        return a + b;
    }
}
