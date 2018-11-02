import java.io.*;
System.out.println("start");
try {
  BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
  String s = br.readLine();
  while (!s.equals("x")) {
    System.out.println("arg0");
    System.out.println(s);
    s = br.readLine();
  }
} catch(IOException e) {
  e.printStackTrace();
}
