select *
from takes, sections, courses
where takes.section_id = sections.id and sections.course_code = courses.course_code and takes.student_id = 'S-1-0001';

select *
from sections, courses
where sections.course_code = courses.course_code and 130 > course_min_credit and 130 < course_max_credit;