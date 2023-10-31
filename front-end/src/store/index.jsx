import { createStore, applyMiddleware, compose } from "redux";
import createSagaMiddleware from "redux-saga";
import { rootSaga, reducers } from "src/redux/index";

const sagaMiddleware = createSagaMiddleware();
const store = createStore(
    reducers,
    process.env.NODE_ENV === "development"
        ? compose(applyMiddleware(sagaMiddleware), window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__())
        : compose(applyMiddleware(sagaMiddleware))
);
sagaMiddleware.run(rootSaga);

export default store;
