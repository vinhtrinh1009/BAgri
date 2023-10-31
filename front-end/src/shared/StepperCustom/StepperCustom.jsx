import { Done } from "@material-ui/icons";
import React, { useState } from "react";

// const steps_data_format = [
//     {
//         name: "Blockchain Config",
//         component: (jumpToStep) => <Step1 jumpToStep={jumpToStep} />,
//     },
//     {
//         name: "Cluster Config",
//         component: (jumpToStep) => (engineBlockchain === "Hyperledger Sawtooth" ? <Step2_sawtooth jumpToStep={jumpToStep} /> : <Step2_fabric jumpToStep={jumpToStep} />),
//     },
//     {
//         name: "Review Config",
//         component: (jumpToStep) => <Step3 jumpToStep={jumpToStep} />,
//     },
// ];

export default function StepperCustom(props) {
    const { steps } = props;
    const [activeStep, setActiveStep] = useState(0);
    const lengthOfSteps = steps.length;

    function getClassNameStepState(indexStep) {
        if (indexStep < activeStep) return "step_done";
        if (indexStep == activeStep) return "step_active";
        if (indexStep > activeStep) return "";
    }

    function jumpToStep(indexStep) {
        setActiveStep(indexStep);
    }

    return (
        <div className="stepper_nav">
            <ul style={{ "--stepslength": lengthOfSteps }}>
                <li className="process" style={{ width: (100 * activeStep) / (lengthOfSteps - 1) + "%" }}></li>
                {steps.map((item, index) => {
                    return (
                        <li key={item?.name + index} className={getClassNameStepState(index)}>
                            <span className="step_name">{item?.name}</span>
                            <span className="step_status_icon step_active">
                                <i className="fa fa-check"></i>
                            </span>
                        </li>
                    );
                })}
            </ul>
            <div className="step_content">{typeof steps[activeStep].component === "function" ? steps[activeStep].component(jumpToStep) : steps[activeStep].component}</div>
        </div>
    );
}
