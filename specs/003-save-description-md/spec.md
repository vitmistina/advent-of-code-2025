# Feature Specification: Save description.md for both AoC parts

**Feature Branch**: `003-save-description-md`  
**Created**: December 1, 2025  
**Status**: Draft  
**Input**: User description: "Save description.md for both AoC parts; support re-download after Part 2 unlocks"

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Save Description on Download (Priority: P1)

As a user, when I download the puzzle for a given day, the system saves the puzzle description to `description.md` in the corresponding day folder.

**Why this priority**: This is the core user expectation and enables reference to the puzzle description offline.

**Independent Test**: Can be fully tested by running the download command and verifying that `description.md` is created and contains the puzzle description.

**Acceptance Scenarios**:

1. **Given** a day folder exists, **When** the user downloads the puzzle, **Then** `description.md` is created with the description content.
2. **Given** a day folder does not exist, **When** the user downloads the puzzle, **Then** the folder and `description.md` are created.

---

### User Story 2 - Overwrite Description After Part 2 Unlock (Priority: P2)

As a user, after solving Part 1 and unlocking Part 2, I can re-download the description and the system overwrites `description.md` with the updated content (now containing both parts).

**Why this priority**: Ensures the user always has the latest, complete puzzle description for both parts.

**Independent Test**: Can be fully tested by downloading before and after unlocking Part 2, and verifying that `description.md` is updated.

**Acceptance Scenarios**:

1. **Given** `description.md` exists with only Part 1, **When** the user re-downloads after unlocking Part 2, **Then** `description.md` is overwritten with the full description.

---

### User Story 3 - Handle Download Failures Gracefully (Priority: P3)

As a user, if the description download fails, the system does not overwrite or create an incomplete `description.md` and provides a clear error message.

**Why this priority**: Prevents data loss and confusion from partial or failed downloads.

**Independent Test**: Can be fully tested by simulating a failed download and verifying that no new or partial file is created.

**Acceptance Scenarios**:

1. **Given** a network or server error, **When** the user attempts to download, **Then** no `description.md` is created or overwritten, and an error is shown.

---

### Edge Cases

- What happens if the user tries to download when the server is unreachable?
- How does the system handle permission errors when writing to the folder?
- What if the description content is empty or malformed?

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST save the downloaded puzzle description to `description.md` in the appropriate day folder on every successful download.
- **FR-002**: System MUST create the day folder if it does not exist before saving `description.md`.
- **FR-003**: System MUST overwrite `description.md` with the latest description content on subsequent downloads (e.g., after Part 2 unlocks).
- **FR-004**: System MUST NOT create or overwrite `description.md` if the download fails or returns invalid content.
- **FR-005**: System MUST provide a clear error message to the user if saving fails (e.g., due to permissions or disk issues).

### Key Entities

- **Day Folder**: Represents the directory for a specific day (e.g., `day-01`).
- **description.md**: Markdown file containing the downloaded puzzle description for the day.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: 100% of successful downloads result in a `description.md` file containing the correct description for the day.
- **SC-002**: 100% of re-downloads after Part 2 unlocks result in `description.md` being updated with the full description.
- **SC-003**: 0% of failed downloads result in a new or overwritten `description.md` file.
- **SC-004**: 100% of error scenarios provide a clear, actionable error message to the user.
