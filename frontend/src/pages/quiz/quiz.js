import React, {useEffect} from 'react';

import classes from "./quiz.module.css";
import { useState } from 'react';

import Navbar from "../../components/navbar";
import ProgressBar from "../../components/progressBar";
import axiosInstance from "../../axios";
import {useLocation} from "react-router-dom";

//page responds for handling quizz data from backend, showing quizz questions and counting the final score
function Quiz() {
    const [questionIndex, setQuestionIndex] = useState(0); //index of question (out of 5)
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [score, setScore] = useState(0);
    const [error, setError] = useState(null);
    const [hasSumbitted , setHasSubmitted] = useState(false);
    const {state} = useLocation(); //use parameters that were given by Leaderboard
    const [questions, setQuestions] = useState(state.questions);
    const [flag, setFlag] = useState(false); //flag for navbar changes
    let maxScore;
    let areaCode = state.location;

    //useEffect to sumbit results only once
    useEffect(() => {
        if (hasSumbitted) {
            sendValues(score,areaCode)
            setFlag(!flag);
        }
    },[hasSumbitted])

    const handleAnswer = (index) => {
        setSelectedAnswer(index);
    };

    //function is triggered when questions are answered
    const handleNext = () => {
        const question = questions[questionIndex];
        if (selectedAnswer !== null && question.answers[selectedAnswer].correct) {
            setScore(score + 1);
        }
        setSelectedAnswer(null);
        setQuestionIndex(questionIndex + 1);

        if (questionIndex >= questions.length-1) {
            setHasSubmitted(true);
        }
    };
    //function sends data of the quiz to log in scores
    const sendValues = (correct, building) => {
        const body = { correct, building };

        axiosInstance.post('quiz/', body)
            .then(response => {
                console.log(response.data);
            })
            .catch(error => {
                console.error(error);
            });
    }

    if(error) {
        return <div>{error.message}</div>;
    }
    //wait until json is loaded
    if(!questions) {
        return (<div>
            Loading... Saving turtles meanwhile...🐢🐢🐢
        </div>)
    }
    maxScore = questions.length;
    //return other view if all questions are answered
    if (questionIndex >= questions.length) {
        return (
            <div className={classes.background}>
                <Navbar flag={flag}/>
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
            <Navbar flag={flag}/>
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