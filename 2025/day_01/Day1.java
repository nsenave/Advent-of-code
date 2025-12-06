import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.Duration;
import java.util.List;

public class Day1 {

    // written with jdk 25
    // javac Day1.java; java Day1
    public static void main(String[] args) {

        var example = parseInput("input-example.txt");
        System.out.println("Example input:");
        printInput(example);

        var puzzle = parseInput("input.txt");

        System.out.println("--- Part One ---");
        Instant start1 = Instant.now();
        System.out.println("Example answer: " + part1(example));
        System.out.println("Puzzle answer:  " + part1(puzzle));
        Instant finish1 = Instant.now();
        System.out.println("Part one computed in " + formatDuration(start1, finish1));

        System.out.println("--- Part Two ---");
        Instant start2 = Instant.now();
        System.out.println("Example answer: " + part2(example));
        System.out.println("Puzzle answer:  " + part2(puzzle));
        Instant finish2 = Instant.now();
        System.out.println("Part two computed in " + formatDuration(start2, finish2));
    }

    static String formatDuration(Instant instantA, Instant instantB) {
        var duration = Duration.between(instantA, instantB);
        long msValue = duration.toMillis();
        return msValue < 1000 ? msValue + " ms" : duration.toSeconds() + " seconds";
    }

    // Input parsing

    enum Direction {
        RIGHT, LEFT;

        static Direction of(String value) {
            return switch (value) {
                case "L" -> LEFT;
                case "R" -> RIGHT;
                default -> throw new IllegalArgumentException(value);
            };
        }
    }

    record Rotation(Direction direction, Integer value) {}

    static List<Rotation> parseInput(String fileName) {
        try {
            var parsed = Files.readAllLines(Path.of(fileName)).stream()
                .map(line -> new Rotation(
                    Direction.of(line.substring(0, 1)), 
                    Integer.parseInt(line.substring(1))))
                .toList();
            System.out.println(fileName + " successfully parsed.");
            return parsed;
        } catch (IOException ioException) {
            System.out.println(ioException.getMessage());
            return null;
        }
    }

    static void printInput(List<Rotation> puzzleInput) {
        puzzleInput.forEach(rotation -> System.out.println(rotation));
    }

    // Part One

    static Integer part1(List<Rotation> rotations) {
        if (rotations == null)
            return null;
        int result = 0;
        int current = 50;
        for (Rotation rotation : rotations) {
            switch (rotation.direction()) {
                case LEFT -> current -= rotation.value();
                case RIGHT -> current += rotation.value();
            }
            current %= 100;
            if (current == 0)
                result ++;
        }
        return result;
    }

    // Part Two

    static Integer part2(List<Rotation> rotations) {
        if (rotations == null)
            return null;
        Clock clock = new Clock();
        return rotations.stream()
            .map(rotation -> clock.rotate(rotation.direction(), rotation.value()))
            .reduce(0, Integer::sum);
    }

    static class Clock {
        private int current = 50;

        public int rotate(Direction direction, int value) {
            int ticks = 0;
            while (value > 0) {
                switch (direction) {
                    case LEFT -> this.current -= 1;
                    case RIGHT -> this.current += 1;
                }
                current %= 100;
                if (current == 0)
                    ticks ++;
                value --;
            }
            return ticks;
        }
    }

}
