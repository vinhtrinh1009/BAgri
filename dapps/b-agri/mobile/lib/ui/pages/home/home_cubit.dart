import 'package:bloc/bloc.dart';
import 'package:equatable/equatable.dart';
import 'package:flutter_base/repositories/weather_repository.dart';

part 'home_state.dart';

class HomeCubit extends Cubit<HomeState> {
  WeatherRepository? weatherRepository;

  HomeCubit({
    this.weatherRepository,
  }) : super(HomeState());
}
