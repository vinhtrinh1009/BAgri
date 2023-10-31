part of 'garden_create_cubit.dart';

class GardenCreateState extends Equatable {
  String? name;
  String? area;
  String? managerId;
  LoadStatus? createGardenStatus;

  GardenCreateState({
    this.name,
    this.area,
    this.managerId,
    this.createGardenStatus,
  });

  GardenCreateState copyWith({
    String? name,
    String? area,
    String? managerId,
    LoadStatus? createGardenStatus,
  }) {
    return GardenCreateState(
      name: name ?? this.name,
      area: area ?? this.area,
      managerId: managerId ?? this.managerId,
      createGardenStatus: createGardenStatus ?? this.createGardenStatus,
    );
  }

  @override
  List<Object?> get props => [
        this.name,
        this.area,
        this.managerId,
        this.createGardenStatus,
      ];
}
