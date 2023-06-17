import { useState, useEffect } from 'react';

interface Props {
    setTurnOver: (value: boolean) => void;
    startTimer: boolean;
    startTime: number;
  }

const Timer = (props: Props) => {
  const [seconds, setSeconds] = useState(0);

  const getTime = () => {
    if(props.startTimer){
        const time = Date.now() - props.startTime;

        setSeconds(Math.floor((time / 1000) % 60));
        if(Math.floor(time/1000) >= 60) {
            props.setTurnOver(true);
        }
    }
  };

  useEffect(() => {
    const interval = setInterval(() => getTime(), 1000);
    
    return () => clearInterval(interval);
  }, [props.startTimer]);

  return (
    <div className="timer">
        {60-seconds}
    </div>
  );
};

export default Timer;