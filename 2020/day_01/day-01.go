package main

import (
    "fmt"
    "log"
    "os"
    "bufio"
    "strconv"
)

func main() {
    exampleNumbers, _ := parseInput("input-example.txt")
    fmt.Printf("Example input: %v\n", exampleNumbers)
    personalNumbers, err := parseInput("input.txt")

    fmt.Println("")

    fmt.Println("--- Part One ---")
    fmt.Println("Example")
    part1(exampleNumbers, nil)
    fmt.Println("Input")
    part1(personalNumbers, err)

    fmt.Println("")

    fmt.Println("--- Part Two ---")
    fmt.Println("Example")
    part2(exampleNumbers, nil)
    fmt.Println("Input")
    part2(personalNumbers, err)
}

// Input parsing

func parseInput(fileName string) ([]int, error) {
    inputFile, err := os.Open(fileName)
    if err != nil {
        log.Printf("%v\n", err)
        return []int{}, err
    }
    defer inputFile.Close()

    scanner := bufio.NewScanner(inputFile)
    var numbers []int

    for scanner.Scan() {
        line := scanner.Text()
        n, err := strconv.Atoi(line)
        if err != nil {
            log.Printf("Error trying to convert: '%s'\n", line)
            log.Fatal(err)
        }
        numbers = append(numbers, n)
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }

    return numbers, nil
}

// Utility functions

func product(numbers []int) int {
    result := 1
    for _, n := range numbers {
        result *= n
    }
    return result
}

// Part One

func part1(numbers []int, parsingError error) {
    if (parsingError != nil) {
        fmt.Println("(input has not been parsed)")
        return
    }
    matchingNumbers := findNumbersThatAddTo2020(numbers)
    fmt.Printf("Matching numbers: %v\n", matchingNumbers)
    fmt.Printf("Answer: %d\n", product(matchingNumbers))
}

func findNumbersThatAddTo2020(numbers []int) []int {
    numbersCount := len(numbers)
    for i := range numbersCount {
        n1 := numbers[i]
        for j := i; j < numbersCount; j++ {
            n2 := numbers[j]
            if (n1 + n2 == 2020) {
                return []int{n1, n2}
            }
        }
    }
    log.Fatal("Didn't find two numbers thats add to 2020.")
    return []int{}
}

// Part Two

func part2(numbers []int, parsingError error) {
    if (parsingError != nil) {
        fmt.Println("(input has not been parsed)")
        return
    }
    matchingNumbers := findThreeNumbersThatAddTo2020(numbers)
    fmt.Printf("Matching numbers: %v\n", matchingNumbers)
    fmt.Printf("Answer: %d\n", product(matchingNumbers))
}

func findThreeNumbersThatAddTo2020(numbers []int) []int {
    numbersCount := len(numbers)
    for i := range numbersCount {
        n1 := numbers[i]
        for j := i; j < numbersCount; j++ {
            n2 := numbers[j]
            for k := j; k < numbersCount; k++ {
                n3 := numbers[k]
                if (n1 + n2 + n3 == 2020) {
                    return []int{n1, n2, n3}
                }
            }
        }
    }
    log.Fatal("Didn't find three numbers thats add to 2020.")
    return []int{}
}
