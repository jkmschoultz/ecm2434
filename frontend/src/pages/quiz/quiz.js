import React, {useEffect} from 'react';

import classes from "./quiz.module.css";
import { useState } from 'react';

import Navbar from "../../components/navbar";
import ProgressBar from "../../components/progressBar";
import {useLocation} from "react-router-dom";

function Quiz() {
    const [questionIndex, setQuestionIndex] = useState(0);
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [score, setScore] = useState(0);
    const [error, setError] = useState(null);
    const [questions, setQuestions] = useState(null);

    // let questions = [
    //     {
    //         text: 'What is the capital of France?',
    //         answers: [
    //             { text: 'Paris', correct: true },
    //             { text: 'Madrid', correct: false },
    //             { text: 'Rome', correct: false },
    //             { text: 'Exeter', correct: false}
    //         ],
    //     },
    //     {
    //         text: 'What is the largest planet in our solar system?',
    //         answers: [
    //             { text: 'Jupiter', correct: true },
    //             { text: 'Venus', correct: false },
    //             { text: 'Saturn', correct: false },
    //             { text: 'Mercury', correct: false}
    //         ],
    //     },
    //     {
    //         text: 'What is the highest mountain in the world?',
    //         answers: [
    //             { text: 'Mount Everest', correct: true },
    //             { text: 'K2', correct: false },
    //             { text: 'Makalu', correct: false },
    //             { text: 'Forum hill', correct: false}
    //         ],
    //     },
    // ];

    const areaCode = useLocation();
    let maxScore;

    useEffect( () => {
            const fetchData = async () => {
                try {
                    const response = await fetch('http://localhost:8000/questions/', {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                    const responseData = await response.json();
                    console.log(responseData);
                    let changedData = responseData.data;
                    console.log(changedData);
                    setQuestions(changedData);
                }
                catch (error) {
                    setError(error);
                }
            }
            fetchData();
    }, []);


    const handleAnswer = (index) => {
        setSelectedAnswer(index);
    };

    const handleNext = () => {
        const question = questions[questionIndex];
        if (selectedAnswer !== null && question.answers[selectedAnswer].correct) {
            setScore(score + 1);
        }
        setSelectedAnswer(null);
        setQuestionIndex(questionIndex + 1);
    };

    if(error) {
        return <div>{error.message}</div>;
    }
    if(!questions) {
        return (<div>Loading</div>)
    }
    maxScore = questions.length;
    if (questionIndex >= questions.length) {
        return (
            <div className={classes.background}>
                <Navbar/>
                <div className={classes.congrats}>
                    You earned {score} points
                </div>
                <div className={classes.progressBar}>
                    <ProgressBar currentPoints={score} maxPoints={maxScore}/>
                </div>
            </div>
        );
    }

    const question = questions[questionIndex];
    return (
        <div className={classes.background}>
            <Navbar/>
            <div className={classes.centre}>
                <div className={classes.question}>{question.text}</div>
                {question.answers.map((answer, index) => (
                    <div key={index} className={classes.answer}>
                        <div
                            className={selectedAnswer === index ? classes.selected : classes.notSelected}
                            onClick={() => handleAnswer(index)}
                        >
                            {answer.text}
                        </div>
                    </div>
                ))}
            </div>
            <button disabled={selectedAnswer === null} onClick={handleNext} className={classes.next}>Next</button>
        </div>
    );
}
export default Quiz;