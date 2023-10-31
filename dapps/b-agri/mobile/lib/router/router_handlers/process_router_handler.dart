import 'package:fluro/fluro.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_base/repositories/process_repository.dart';
import 'package:flutter_base/ui/pages/process_management/add_process/add_process_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/add_process/add_process_page.dart';
import 'package:flutter_base/ui/pages/process_management/process_detail/process_detail_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/process_detail/process_detail_page.dart';
import 'package:flutter_base/ui/pages/process_management/process_listing/process_listing_page.dart';
import 'package:flutter_base/ui/pages/process_management/process_season/process_season_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/process_season/process_season_page.dart';
import 'package:flutter_base/ui/pages/process_management/tab_process_tree.dart';
import 'package:flutter_base/ui/pages/process_management/update_process/update_process_cubit.dart';
import 'package:flutter_base/ui/pages/process_management/update_process/update_process_page.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

Handler tabProcessHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return ProcessTabPage();
});

Handler processListHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return ProcessListPage();
});

Handler processCreateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  return BlocProvider(
    create: (context) {
      final processRepository =
          RepositoryProvider.of<ProcessRepository>(context);
      return AddProcessCubit(processRepository: processRepository);
    },
    child: ProcessAddingPage(),
  );
});

Handler processUpdateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  ProcessUpdateArgument args =
      context!.settings!.arguments as ProcessUpdateArgument;
  return BlocProvider(
    create: (context) {
      final processRepository =
          RepositoryProvider.of<ProcessRepository>(context);
      return UpdateProcessCubit(processRepository: processRepository);
    },
    child: UpdateProcessPage(
      process_id: args.process_id,
    ),
  );
});

Handler processDetailHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  ProcessDetailArgument args =
      context!.settings!.arguments as ProcessDetailArgument;
  return BlocProvider(
    create: (context) {
      final processRepository =
          RepositoryProvider.of<ProcessRepository>(context);
      return ProcessDetailCubit(processRepository: processRepository);
    },
    child: ProcessDetailPage(
      process_id: args.process_id,
    ),
  );
});

Handler processSeasonUpdateHandler = new Handler(
    handlerFunc: (BuildContext? context, Map<String, List<String>> params) {
  ProcessSeasonArgument args =
      context!.settings!.arguments as ProcessSeasonArgument;
  return BlocProvider(
    create: (context) {
      final processRepository =
          RepositoryProvider.of<ProcessRepository>(context);
      return ProcessSeasonCubit(processRepository: processRepository);
    },
    child: UpdateProcessSeasonPage(
      process_id: args.process_id,
    ),
  );
});
