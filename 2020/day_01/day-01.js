const parseInput = function (content) {
    result = []
    for (const strNumber of content.split('\n')) {
        result.push(parseInt(strNumber))
    }
    return result
}

const findNumbersThatAddTo2020 = function (numbers) {
    for (let i = 0; i < numbers.length; i++) {
        const number1 = numbers[i]
        for (let j = 0; j < numbers.length; j++) {
            const number2 = numbers[j]
            if (number1 + number2 === 2020)
                return [number1, number2]
        }
    }
    throw Error("Didn't find two matching numbers.")
}

const findThreeNumbersThatAddTo2020 = function (numbers) {
    for (let i = 0; i < numbers.length; i++) {
        const number1 = numbers[i]
        for (let j = 0; j < numbers.length; j++) {
            const number2 = numbers[j]
            for (let k = 0; k < numbers.length; k++) {
                const number3 = numbers[k]
                    if (number1 + number2 + number3 === 2020)
                        return [number1, number2, number3]
            }
        }
    }
    throw Error("Didn't find three matching numbers.")
}

const numbersProduct = function(numbers) {
    return numbers.reduce((accumulator, current) => accumulator * current, 1)
}

const computeAndAttachSolution = function (numbers, findFunction, resultNumbersId, resultId) {
    const matchingNumbers = findFunction(numbers)
    document.getElementById(resultNumbersId).innerText = matchingNumbers
    document.getElementById(resultId).innerText = numbersProduct(matchingNumbers)
}

document.getElementById('exampleInput').addEventListener('change', function(event) {
    const file = event.target.files[0]
    if (!file) {
        console.log('Example input file not received!')
        return
    }
    const reader = new FileReader()
    reader.onload = function(progressEvent) {
        const exampleContent = progressEvent.target.result
        document.getElementById('exampleRaw').innerText = exampleContent
        const numbers = parseInput(exampleContent)
        document.getElementById('exampleParsed').innerText = numbers
        computeAndAttachSolution(numbers, findNumbersThatAddTo2020, 'exampleResultNumbers1', 'exampleResult1')
        computeAndAttachSolution(numbers, findThreeNumbersThatAddTo2020, 'exampleResultNumbers2', 'exampleResult2')
    }
    reader.readAsText(file)
})

document.getElementById('input').addEventListener('change', function(event) {
    const file = event.target.files[0]
    if (!file) {
        console.log('Input file not received!')
        return
    }
    const reader = new FileReader()
    reader.onload = function(progressEvent) {
        const numbers = parseInput(progressEvent.target.result)
        console.log('Numbers count in input: ' + numbers.length)
        computeAndAttachSolution(numbers, findNumbersThatAddTo2020, 'resultNumbers1', 'result1')
        computeAndAttachSolution(numbers, findThreeNumbersThatAddTo2020, 'resultNumbers2', 'result2')
    }
    reader.readAsText(file)
})
