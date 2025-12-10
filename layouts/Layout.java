import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Instant;
import java.time.Duration;
import java.util.List;

// requires: jdk 25+
// java Layout.java

void main() {

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

String formatDuration(Instant instantA, Instant instantB) {
    var duration = Duration.between(instantA, instantB);
    long msValue = duration.toMillis();
    return msValue < 1000 ? msValue + " ms" : duration.toSeconds() + " seconds";
}

// Input parsing

List<Object> parseInput(String fileName) {
    try {
        var parsed = Files.readAllLines(Path.of(fileName)).stream()
            .map(line -> (Object) line)
            .toList();
        System.out.println(fileName + " successfully parsed.");
        return parsed;
    } catch (IOException ioException) {
        System.out.println(ioException.getMessage());
        return null;
    }
}

void printInput(List<Object> puzzleInput) {
    System.out.println(puzzleInput);
}

// Part One

Long part1(List<Object> puzzleInput) {
    if (puzzleInput == null)
        return null;
    long result = 0;
    for (var object : puzzleInput) {
        //
    }
    return result;
}

// Part Two

Long part2(List<Object> puzzleInput) {
    if (puzzleInput == null)
        return null;
    long result = 0;
    for (var object : puzzleInput) {
        //
    }
    return result;
}
