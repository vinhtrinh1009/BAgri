import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/models/entities/season/season_entity.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/repositories/season_repository.dart';
import 'package:flutter_base/ui/pages/seasons_management/add_season/season_adding_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/add_season/season_adding_page.dart';
import 'package:flutter_base/ui/pages/seasons_management/season_management_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/season_management_page.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/season_detail_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/seasons_detail/season_detail_page.dart';
import 'package:flutter_base/ui/pages/seasons_management/update_season/season_updating_cubit.dart';
import 'package:flutter_base/ui/pages/seasons_management/update_season/season_updating_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Handler seasonManagementHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      SeasonRepository seasonRepository =
          RepositoryProvider.of<SeasonRepository>(context);
      return SeasonManagementCubit(seasonRepository: seasonRepository);
    },
    child: SeasonTabPage(),
  );
});

Handler seasonAddingHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      SeasonRepository seasonRepository =
          RepositoryProvider.of<SeasonRepository>(context);
      ProcessRepository processRepository =
          RepositoryProvider.of<ProcessRepository>(context);
      return SeasonAddingCubit(
          seasonRepository: seasonRepository,
          processRepository: processRepository);
    },
    child: SeasonAddingPage(),
  );
});

Handler seasonDetailHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  SeasonEntity argument = context!.settings!.arguments as SeasonEntity;
  return BlocProvider(
    create: (context) {
      SeasonRepository seasonRepository =
          RepositoryProvider.of<SeasonRepository>(context);
      return SeasonDetailCubit(seasonRepository: seasonRepository);
    },
    child: SeasonDetailPage(
      thisSeason: argument,
    ),
  );
});

Handler seasonUpdatingHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  String seasonId = context!.settings!.arguments as String;
  return BlocProvider(
    create: (context) {
      SeasonRepository seasonRepository =
          RepositoryProvider.of<SeasonRepository>(context);
      ProcessRepository processRepository =
          RepositoryProvider.of<ProcessRepository>(context);
      return SeasonUpdatingCubit(
          seasonRepository: seasonRepository,
          processRepository: processRepository);
    },
    child: SeasonUpdatingPage(seasonId: seasonId),
  );
});
