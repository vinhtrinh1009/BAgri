import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/router/application.dart';
import 'package:flutter_base/router/routers.dart';

part 'navigation_state.dart';

class NavigationCubit extends Cubit<NavigationState> {
  NavigationCubit() : super(NavigationState.initial());

  void setCurrentScreen(String screenName) {
    List<String> currentStack = state.routeStack ?? [];
    currentStack.add(screenName);
    Application.routeStack.add(screenName);
    emit(state.copyWith(currentRoute: screenName, routeStack: currentStack));
  }

  void removeCurrentScreen(String screenName) {
    List<String> currentStack = state.routeStack ?? [];
    if (currentStack.length > 0) {
      currentStack.removeLast();
      Application.routeStack.removeLast();
    }
    emit(state.copyWith(currentRoute: screenName, routeStack: currentStack));
  }
}
