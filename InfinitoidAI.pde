import java.io.*;

void setup() {
  size(1000, 1000);
  System.out.println("RUNTIME: Processing render subprocess started.");
  try {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    fill(255, 0, 0);
    ellipse(100, 100, 100, 100);
    String s = br.readLine();
    while (!s.equals("x")) {
      System.out.println("RENDER: got input: " + s);
      s = br.readLine();
    }
    System.out.println("RUNTIME: Processing render subprocess terminated.");
  } catch(IOException e) {
    e.printStackTrace();
  }
  exit();
}
