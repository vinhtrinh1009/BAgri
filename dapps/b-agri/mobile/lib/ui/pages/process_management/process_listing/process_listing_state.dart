part of 'process_listing_cubit.dart';

class ProcessListState extends Equatable {
  LoadStatus? getProcessStatus;
  LoadStatus? deleteProcessStatus;
  List<ProcessEntity>? listData;

  ProcessListState(
      {this.getProcessStatus, this.listData, this.deleteProcessStatus});

  ProcessListState copyWith({
    LoadStatus? getProcessStatus,
    List<ProcessEntity>? listData,
    LoadStatus? deleteProcessStatus,
  }) {
    return ProcessListState(
      getProcessStatus: getProcessStatus ?? this.getProcessStatus,
      listData: listData ?? this.listData,
      deleteProcessStatus: deleteProcessStatus ?? this.deleteProcessStatus,
    );
  }

  @override
  List<Object?> get props =>
      [this.getProcessStatus, this.listData, this.deleteProcessStatus];
}
