# Data Model: Day 3 Part 2

## Entities

### Bank

- **Attributes**: digits (str or list[int])
- **Description**: Sequence of battery digits (1-9)

### SelectedBatteries

- **Attributes**: indices (list[int]), values (list[int])
- **Description**: Indices and values of the 12 selected batteries

### OutputJoltage

- **Attributes**: value (int)
- **Description**: Integer formed by concatenating selected digits

## Relationships

- Each Bank produces one OutputJoltage by selecting 12 batteries
