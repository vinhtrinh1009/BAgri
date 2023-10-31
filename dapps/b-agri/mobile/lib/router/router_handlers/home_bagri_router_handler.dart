import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/repositories/weather_repository.dart';
import 'package:flutter_base/ui/pages/home/home_cubit.dart';
import 'package:flutter_base/ui/pages/home/home_page.dart';

import 'package:flutter_bloc/flutter_bloc.dart';

Handler homeHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final weatherRepository =
          RepositoryProvider.of<WeatherRepository>(context);
      return HomeCubit(weatherRepository: weatherRepository);
    },
    child: HomePage(),
  );
});
