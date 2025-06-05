package fr.nsenave;

import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {

        String input = """
                3   4
                4   3
                2   5
                1   3
                3   9
                3   3""";

        String[] lines = input.split("\n");
        for (String line : lines) {
            String[] numbers = line.split("   ");
            System.out.println("Nombres " + numbers[0] + ", " + numbers[1]);
        }
    }
}