package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

type IdRange struct {
    start int
    end int
}

func main() {

    exampleInput := parseInput("input-example.txt")
    fmt.Println("Example input:")
    printInput(exampleInput)

    personalInput := parseInput("input.txt")

    fmt.Println("--- Part One ---")
    start1 := time.Now()
    fmt.Printf("Example answer: %d\n", part1(exampleInput, true))
    fmt.Printf("Puzzle answer:  %d\n", part1(personalInput))
    end1 := time.Now()
    fmt.Printf("Part one computed in %v.\n", end1.Sub(start1))

    fmt.Println("--- Part Two ---")
    start2 := time.Now()
    fmt.Printf("Example result: %d\n", part2(exampleInput, true))
    fmt.Printf("Puzzle answer:  %d\n", part2(personalInput))
    end2 := time.Now()
    fmt.Printf("Part two computed in %v.\n", end2.Sub(start2))
}

// Input parsing

func parseInput(fileName string) []IdRange {
    content, err := os.ReadFile(fileName)
    if (err != nil) {
        log.Println(err)
        return nil
    }
    var puzzleInput []IdRange
    for stringRange := range strings.SplitSeq(string(content), ",") {
        puzzleInput = append(puzzleInput, parseRange(stringRange))
    }
    log.Printf("%s input successfully parsed.\n", fileName)
    return puzzleInput
}

func parseRange(stringRange string) IdRange {
    ids := strings.Split(stringRange, "-")
    return IdRange{toInt(ids[0]), toInt(ids[1])}
}

func printInput(puzzleInput []IdRange) {
    fmt.Printf("%v\n", puzzleInput)
}

// Utility functions

func toInt(s string) int {
    result, err := strconv.Atoi(s)
    if (err != nil) {
        log.Fatal(err)
    }
    return result
}

func toString(i int) string {
    return strconv.Itoa(i)
}

func optionalBool(param []bool) bool {
    if len(param) > 0 {
        return param[0]
    }
    return false
}

// Solution

func solve(puzzleInput []IdRange, isInvalidFunc func(int) bool, debug bool) int {
    if (puzzleInput == nil) {
        return 0
    }
    result := 0
    var invalidIds []int
    for _, idRange := range puzzleInput {
        for id := idRange.start; id <= idRange.end; id++ {
            if isInvalidFunc(id) {
                result += id
                if debug {
                    invalidIds = append(invalidIds, id)
                }
            }
        }
    }
    if debug {
        fmt.Printf("Invalid ids: %v\n", invalidIds)
    }
    return result
}

func part1(puzzleInput []IdRange, debug ...bool) int {
    return solve(puzzleInput, isInvalid, optionalBool(debug))
}

func part2(puzzleInput []IdRange, debug ...bool) int {
    return solve(puzzleInput, isInvalid2, optionalBool(debug))
}

func isInvalid(id int) bool {
    stringId := toString(id)
    idLength := len(stringId)
    if (idLength % 2 != 0) {
        return false
    }
    half := idLength / 2
    return stringId[:half] == stringId[half:]
}

func isInvalid2(id int) bool {
    stringId := toString(id)
    idLength := len(stringId)
    middle := idLength / 2
    for d := 1; d <= middle; d++ {
        if idLength % d != 0 {
            continue
        }
        pattern := stringId[:d]
        if strings.Repeat(pattern, idLength / d) == stringId {
            return true;
        }
    } 
    return false
}
