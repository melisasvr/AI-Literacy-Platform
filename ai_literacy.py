"""
AI Literacy Platform - Core Structure (FIXED)
A comprehensive platform for teaching AI literacy through interactive modules and scenario-based learning.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import uuid
from datetime import datetime, timedelta
import random

# Core Data Models
class UserRole(Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class DifficultyLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ModuleCategory(Enum):
    AI_BASICS = "ai_basics"
    APPLICATIONS = "applications"
    ETHICS_BIAS = "ethics_bias"
    CRITICAL_THINKING = "critical_thinking"
    PRACTICAL_SKILLS = "practical_skills"

@dataclass
class User:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str = ""
    email: str = ""
    role: UserRole = UserRole.STUDENT
    created_at: datetime = field(default_factory=datetime.now)
    learning_preferences: Dict[str, Any] = field(default_factory=dict)
    progress: Dict[str, float] = field(default_factory=dict)  # module_id -> completion %

@dataclass
class LearningModule:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    category: ModuleCategory = ModuleCategory.AI_BASICS
    difficulty: DifficultyLevel = DifficultyLevel.BEGINNER
    prerequisites: List[str] = field(default_factory=list)
    content_blocks: List[Dict[str, Any]] = field(default_factory=list)
    scenarios: List[Dict[str, Any]] = field(default_factory=list)
    assessment_questions: List[Dict[str, Any]] = field(default_factory=list)
    estimated_duration: int = 30  # minutes

@dataclass
class Scenario:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    description: str = ""
    context: str = ""
    challenge: str = ""
    options: List[Dict[str, Any]] = field(default_factory=list)
    ethical_considerations: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)

@dataclass
class UserProgress:
    user_id: str = ""
    module_id: str = ""
    completion_percentage: float = 0.0
    time_spent: int = 0  # minutes
    last_accessed: datetime = field(default_factory=datetime.now)
    quiz_scores: List[float] = field(default_factory=list)
    scenario_completions: List[str] = field(default_factory=list)

class AILiteracyPlatform:
    """Main platform class managing users, modules, and learning paths."""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.modules: Dict[str, LearningModule] = {}
        self.scenarios: Dict[str, Scenario] = {}
        self.user_progress: Dict[str, Dict[str, UserProgress]] = {}
        self._initialize_sample_content()
    
    def _initialize_sample_content(self):
        """Initialize the platform with sample modules and scenarios."""
        
        # Sample AI Basics Module
        ai_basics = LearningModule(
            title="Introduction to Artificial Intelligence",
            description="Foundational concepts of AI, machine learning, and their real-world applications",
            category=ModuleCategory.AI_BASICS,
            difficulty=DifficultyLevel.BEGINNER,
            content_blocks=[
                {
                    "type": "text",
                    "title": "What is AI?",
                    "content": "Artificial Intelligence refers to computer systems that can perform tasks typically requiring human intelligence..."
                },
                {
                    "type": "interactive",
                    "title": "AI vs Machine Learning vs Deep Learning",
                    "content": "Interactive diagram showing the relationship between these concepts"
                },
                {
                    "type": "video",
                    "title": "AI in Daily Life",
                    "content": "Examples of AI applications you encounter every day"
                }
            ],
            assessment_questions=[
                {
                    "question": "Which of the following is NOT a type of machine learning?",
                    "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Quantum Learning"],
                    "correct": 3,
                    "explanation": "Quantum Learning is not a recognized type of machine learning paradigm."
                }
            ]
        )
        
        # Sample Ethics Module
        ethics_module = LearningModule(
            title="AI Ethics and Bias",
            description="Understanding ethical implications, bias detection, and responsible AI use",
            category=ModuleCategory.ETHICS_BIAS,
            difficulty=DifficultyLevel.INTERMEDIATE,
            prerequisites=[ai_basics.id],
            content_blocks=[
                {
                    "type": "case_study",
                    "title": "Algorithmic Bias in Hiring",
                    "content": "Real-world examples of how AI systems can perpetuate discrimination"
                },
                {
                    "type": "interactive",
                    "title": "Bias Detection Exercise",
                    "content": "Interactive tool to identify potential bias in AI systems"
                }
            ]
        )
        
        # Sample Scenario
        hiring_scenario = Scenario(
            title="AI-Powered Hiring System",
            description="You're implementing an AI system to screen job applications",
            context="Your company wants to automate the initial screening of resumes using AI to save time and reduce human bias.",
            challenge="How do you ensure the AI system doesn't discriminate against qualified candidates?",
            options=[
                {
                    "text": "Use historical hiring data to train the model",
                    "consequence": "Risk of perpetuating past biases",
                    "ethics_score": 2
                },
                {
                    "text": "Implement bias detection and regular auditing",
                    "consequence": "Better fairness but requires ongoing monitoring",
                    "ethics_score": 8
                },
                {
                    "text": "Focus only on technical skills and ignore demographics",
                    "consequence": "May miss important soft skills and context",
                    "ethics_score": 6
                }
            ],
            ethical_considerations=[
                "Fairness and non-discrimination",
                "Transparency in decision-making",
                "Accountability for AI decisions"
            ],
            learning_objectives=[
                "Identify potential sources of bias in AI systems",
                "Understand the importance of diverse training data",
                "Learn strategies for ongoing bias monitoring"
            ]
        )
        
        self.modules[ai_basics.id] = ai_basics
        self.modules[ethics_module.id] = ethics_module
        self.scenarios[hiring_scenario.id] = hiring_scenario
    
    def create_user(self, username: str, email: str, role: UserRole = UserRole.STUDENT) -> User:
        """Create a new user account."""
        user = User(username=username, email=email, role=role)
        self.users[user.id] = user
        self.user_progress[user.id] = {}
        return user
    
    def get_personalized_learning_path(self, user_id: str) -> List[LearningModule]:
        """Generate a personalized learning path based on user progress and preferences."""
        user = self.users.get(user_id)
        if not user:
            return []
        
        # Get user's current progress
        completed_modules = {
            module_id for module_id, progress in user.progress.items() 
            if progress >= 90.0
        }
        
        # Find available modules (prerequisites met)
        available_modules = []
        for module in self.modules.values():
            if module.id not in completed_modules:
                prerequisites_met = all(
                    prereq in completed_modules 
                    for prereq in module.prerequisites
                )
                if prerequisites_met:
                    available_modules.append(module)
        
        # Sort by difficulty and category preferences
        def sort_key(module):
            difficulty_order = {
                DifficultyLevel.BEGINNER: 1,
                DifficultyLevel.INTERMEDIATE: 2,
                DifficultyLevel.ADVANCED: 3
            }
            return (difficulty_order[module.difficulty], module.title)
        
        return sorted(available_modules, key=sort_key)
    
    def update_progress(self, user_id: str, module_id: str, completion_percentage: float, 
                       time_spent: int = 0) -> bool:
        """Update user's progress on a specific module."""
        if user_id not in self.users or module_id not in self.modules:
            return False
        
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        if module_id not in self.user_progress[user_id]:
            self.user_progress[user_id][module_id] = UserProgress(
                user_id=user_id, 
                module_id=module_id
            )
        
        progress = self.user_progress[user_id][module_id]
        progress.completion_percentage = max(progress.completion_percentage, completion_percentage)
        progress.time_spent += time_spent
        progress.last_accessed = datetime.now()
        
        # Update user's overall progress
        self.users[user_id].progress[module_id] = completion_percentage
        
        return True
    
    def get_adaptive_feedback(self, user_id: str, module_id: str, 
                           user_response: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered adaptive feedback based on user performance."""
        user = self.users.get(user_id)
        module = self.modules.get(module_id)
        
        if not user or not module:
            return {"error": "User or module not found"}
        
        # Simple adaptive feedback logic (in practice, this would use ML models)
        feedback = {
            "message": "",
            "suggestions": [],
            "next_steps": [],
            "difficulty_adjustment": 0
        }
        
        # Analyze user's response pattern
        if user_id in self.user_progress and module_id in self.user_progress[user_id]:
            progress = self.user_progress[user_id][module_id]
            avg_score = sum(progress.quiz_scores) / len(progress.quiz_scores) if progress.quiz_scores else 0
            
            if avg_score < 60:
                feedback["message"] = "Consider reviewing the foundational concepts before moving forward."
                feedback["suggestions"] = [
                    "Revisit the basic definitions",
                    "Try the interactive exercises again",
                    "Watch supplementary videos"
                ]
                feedback["difficulty_adjustment"] = -1
            elif avg_score > 85:
                feedback["message"] = "Excellent work! You're ready for more advanced topics."
                feedback["suggestions"] = [
                    "Explore advanced scenarios",
                    "Try the challenge problems",
                    "Consider peer tutoring opportunities"
                ]
                feedback["difficulty_adjustment"] = 1
            else:
                feedback["message"] = "Good progress! Keep practicing to solidify your understanding."
                feedback["suggestions"] = [
                    "Complete additional practice scenarios",
                    "Review areas where you scored lower"
                ]
        
        return feedback
    
    def get_teacher_dashboard_data(self, teacher_id: str) -> Dict[str, Any]:
        """Generate dashboard data for teachers to track student progress."""
        teacher = self.users.get(teacher_id)
        if not teacher or teacher.role != UserRole.TEACHER:
            return {"error": "Access denied"}
        
        # In a real system, teachers would be associated with specific classes/students
        students = [user for user in self.users.values() if user.role == UserRole.STUDENT]
        
        dashboard_data = {
            "total_students": len(students),
            "student_progress": [],
            "module_completion_rates": {},
            "common_challenges": [],
            "recommendations": []
        }
        
        # Calculate student progress - FIXED VERSION
        for student in students:
            total_modules = len(self.modules)
            
            # Calculate average completion percentage across all modules
            if student.progress:
                # Average the completion percentages of all modules the student has started
                avg_completion = sum(student.progress.values()) / len(student.progress)
            else:
                avg_completion = 0.0
            
            # Get total time spent from UserProgress objects
            total_time_spent = 0
            last_active = student.created_at
            
            if student.id in self.user_progress:
                for module_progress in self.user_progress[student.id].values():
                    total_time_spent += module_progress.time_spent
                    if module_progress.last_accessed > last_active:
                        last_active = module_progress.last_accessed
            
            dashboard_data["student_progress"].append({
                "student_name": student.username,
                "completion_rate": avg_completion,  # This now shows the actual average completion
                "time_spent": total_time_spent,
                "last_active": last_active
            })
        
        # Calculate module completion rates (students who completed >= 90%)
        for module_id, module in self.modules.items():
            completed_count = sum(
                1 for student in students
                if student.progress.get(module_id, 0) >= 90.0
            )
            dashboard_data["module_completion_rates"][module.title] = (
                (completed_count / len(students)) * 100 if students else 0
            )
        
        return dashboard_data
    
    def save_platform_data(self, filename: str = "ai_literacy_data.json") -> bool:
        """Save platform data to JSON file for persistence."""
        try:
            data = {
                "users": {
                    user_id: {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "role": user.role.value,
                        "created_at": user.created_at.isoformat(),
                        "learning_preferences": user.learning_preferences,
                        "progress": user.progress
                    }
                    for user_id, user in self.users.items()
                },
                "modules": {
                    module_id: {
                        "id": module.id,
                        "title": module.title,
                        "description": module.description,
                        "category": module.category.value,
                        "difficulty": module.difficulty.value,
                        "prerequisites": module.prerequisites,
                        "content_blocks": module.content_blocks,
                        "scenarios": module.scenarios,
                        "assessment_questions": module.assessment_questions,
                        "estimated_duration": module.estimated_duration
                    }
                    for module_id, module in self.modules.items()
                },
                "user_progress": {
                    user_id: {
                        module_id: {
                            "user_id": progress.user_id,
                            "module_id": progress.module_id,
                            "completion_percentage": progress.completion_percentage,
                            "time_spent": progress.time_spent,
                            "last_accessed": progress.last_accessed.isoformat(),
                            "quiz_scores": progress.quiz_scores,
                            "scenario_completions": progress.scenario_completions
                        }
                        for module_id, progress in user_modules.items()
                    }
                    for user_id, user_modules in self.user_progress.items()
                }
            }
            
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_platform_data(self, filename: str = "ai_literacy_data.json") -> bool:
        """Load platform data from JSON file."""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Load users
            self.users = {}
            for user_id, user_data in data.get("users", {}).items():
                user = User(
                    id=user_data["id"],
                    username=user_data["username"],
                    email=user_data["email"],
                    role=UserRole(user_data["role"]),
                    created_at=datetime.fromisoformat(user_data["created_at"]),
                    learning_preferences=user_data["learning_preferences"],
                    progress=user_data["progress"]
                )
                self.users[user_id] = user
            
            # Load modules
            self.modules = {}
            for module_id, module_data in data.get("modules", {}).items():
                module = LearningModule(
                    id=module_data["id"],
                    title=module_data["title"],
                    description=module_data["description"],
                    category=ModuleCategory(module_data["category"]),
                    difficulty=DifficultyLevel(module_data["difficulty"]),
                    prerequisites=module_data["prerequisites"],
                    content_blocks=module_data["content_blocks"],
                    scenarios=module_data["scenarios"],
                    assessment_questions=module_data["assessment_questions"],
                    estimated_duration=module_data["estimated_duration"]
                )
                self.modules[module_id] = module
            
            # Load user progress
            self.user_progress = {}
            for user_id, user_modules in data.get("user_progress", {}).items():
                self.user_progress[user_id] = {}
                for module_id, progress_data in user_modules.items():
                    progress = UserProgress(
                        user_id=progress_data["user_id"],
                        module_id=progress_data["module_id"],
                        completion_percentage=progress_data["completion_percentage"],
                        time_spent=progress_data["time_spent"],
                        last_accessed=datetime.fromisoformat(progress_data["last_accessed"]),
                        quiz_scores=progress_data["quiz_scores"],
                        scenario_completions=progress_data["scenario_completions"]
                    )
                    self.user_progress[user_id][module_id] = progress
            
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_student_analytics(self, student_id: str) -> Dict[str, Any]:
        """Get detailed analytics for a specific student."""
        student = self.users.get(student_id)
        if not student or student.role != UserRole.STUDENT:
            return {"error": "Student not found"}
        
        analytics = {
            "student_info": {
                "name": student.username,
                "email": student.email,
                "join_date": student.created_at.strftime("%Y-%m-%d")
            },
            "overall_progress": 0.0,
            "total_time_spent": 0,
            "modules_completed": 0,
            "modules_in_progress": 0,
            "average_quiz_score": 0.0,
            "learning_streak": 0,
            "strengths": [],
            "areas_for_improvement": [],
            "next_recommendations": []
        }
        
        if student_id in self.user_progress:
            total_progress = 0
            total_time = 0
            all_quiz_scores = []
            modules_completed = 0
            modules_in_progress = 0
            
            for module_id, progress in self.user_progress[student_id].items():
                total_progress += progress.completion_percentage
                total_time += progress.time_spent
                all_quiz_scores.extend(progress.quiz_scores)
                
                if progress.completion_percentage >= 90:
                    modules_completed += 1
                elif progress.completion_percentage > 0:
                    modules_in_progress += 1
            
            total_modules = len(self.user_progress[student_id])
            if total_modules > 0:
                analytics["overall_progress"] = total_progress / total_modules
            
            analytics["total_time_spent"] = total_time
            analytics["modules_completed"] = modules_completed
            analytics["modules_in_progress"] = modules_in_progress
            
            if all_quiz_scores:
                analytics["average_quiz_score"] = sum(all_quiz_scores) / len(all_quiz_scores)
        
        return analytics
    
    def recommend_next_module(self, user_id: str) -> Optional[LearningModule]:
        """Recommend the next best module for a user based on their progress and performance."""
        user = self.users.get(user_id)
        if not user:
            return None
        
        available_modules = self.get_personalized_learning_path(user_id)
        if not available_modules:
            return None
        
        # Simple recommendation logic - can be enhanced with ML
        # Prioritize modules based on user's performance in similar categories
        user_progress = self.user_progress.get(user_id, {})
        
        # Calculate average performance by category
        category_performance = {}
        for module_id, progress in user_progress.items():
            module = self.modules.get(module_id)
            if module and progress.quiz_scores:
                category = module.category
                avg_score = sum(progress.quiz_scores) / len(progress.quiz_scores)
                if category not in category_performance:
                    category_performance[category] = []
                category_performance[category].append(avg_score)
        
        # Find the best next module
        best_module = available_modules[0]  # Default to first available
        
        # Prefer modules in categories where user performs well
        for module in available_modules:
            if module.category in category_performance:
                avg_category_score = sum(category_performance[module.category]) / len(category_performance[module.category])
                if avg_category_score > 75:  # Good performance threshold
                    best_module = module
                    break
        
        return best_module

# Example Usage and Testing
def demo_platform():
    """Demonstrate the AI Literacy Platform functionality."""
    platform = AILiteracyPlatform()
    
    # Create users
    student = platform.create_user("alice_student", "alice@example.com", UserRole.STUDENT)
    teacher = platform.create_user("bob_teacher", "bob@example.com", UserRole.TEACHER)
    
    print(f"Created student: {student.username} (ID: {student.id})")
    print(f"Created teacher: {teacher.username} (ID: {teacher.id})")
    
    # Get learning path for student
    learning_path = platform.get_personalized_learning_path(student.id)
    print(f"\nPersonalized learning path for {student.username}:")
    for i, module in enumerate(learning_path, 1):
        print(f"{i}. {module.title} ({module.difficulty.value})")
    
    # Simulate progress
    if learning_path:
        first_module = learning_path[0]
        platform.update_progress(student.id, first_module.id, 45.0, 25)
        platform.update_progress(student.id, first_module.id, 75.0, 20)
        
        # Get adaptive feedback
        feedback = platform.get_adaptive_feedback(
            student.id, 
            first_module.id, 
            {"quiz_score": 78, "time_spent": 45}
        )
        print(f"\nAdaptive feedback: {feedback['message']}")
        print("Suggestions:", feedback['suggestions'])
    
    # Teacher dashboard
    dashboard = platform.get_teacher_dashboard_data(teacher.id)
    print(f"\nTeacher Dashboard:")
    print(f"Total students: {dashboard['total_students']}")
    print("Student progress:", dashboard['student_progress'])

def demo_new_features():
    """Demonstrate the new features added to the platform."""
    platform = AILiteracyPlatform()
    
    # Create test users
    student = platform.create_user("test_student", "student@test.com", UserRole.STUDENT)
    teacher = platform.create_user("test_teacher", "teacher@test.com", UserRole.TEACHER)
    
    # Add some progress
    ai_basics_id = list(platform.modules.keys())[0]
    platform.update_progress(student.id, ai_basics_id, 85.0, 60)
    
    # Add quiz scores
    if student.id in platform.user_progress and ai_basics_id in platform.user_progress[student.id]:
        platform.user_progress[student.id][ai_basics_id].quiz_scores = [78, 82, 88, 85]
    
    print("🔍 STUDENT ANALYTICS EXAMPLE:")
    analytics = platform.get_student_analytics(student.id)
    print(f"Student: {analytics['student_info']['name']}")
    print(f"Overall Progress: {analytics['overall_progress']:.1f}%")
    print(f"Total Time Spent: {analytics['total_time_spent']} minutes")
    print(f"Average Quiz Score: {analytics['average_quiz_score']:.1f}")
    print(f"Modules Completed: {analytics['modules_completed']}")
    print(f"Modules In Progress: {analytics['modules_in_progress']}")
    
    print("\n🎯 MODULE RECOMMENDATION:")
    recommended = platform.recommend_next_module(student.id)
    if recommended:
        print(f"Recommended: {recommended.title}")
        print(f"Difficulty: {recommended.difficulty.value}")
        print(f"Category: {recommended.category.value}")
    
    print("\n💾 DATA PERSISTENCE TEST:")
    # Test saving data
    if platform.save_platform_data("test_data.json"):
        print("✅ Data saved successfully!")
        
        # Create new platform and load data
        new_platform = AILiteracyPlatform()
        if new_platform.load_platform_data("test_data.json"):
            print("✅ Data loaded successfully!")
            print(f"Loaded {len(new_platform.users)} users and {len(new_platform.modules)} modules")
        else:
            print("❌ Failed to load data")
    else:
        print("❌ Failed to save data")

if __name__ == "__main__":
    # Run the basic demo first
    print("🚀 BASIC DEMO OUTPUT:")
    print("="*40)
    demo_platform()
    
    # Demonstrate new features
    print("\n🆕 NEW FEATURES DEMONSTRATION:")
    print("="*50)
    demo_new_features()
    
    # Then run the enhanced demo
    print("\n🚀 ENHANCED PLATFORM DEMONSTRATION:")
    print("="*60)
    
    platform = AILiteracyPlatform()
    
    # Create sample users with more realistic data
    students = [
        platform.create_user("emma_chen", "emma@school.edu", UserRole.STUDENT),
        platform.create_user("james_wilson", "james@school.edu", UserRole.STUDENT),
        platform.create_user("maria_garcia", "maria@school.edu", UserRole.STUDENT)
    ]
    teacher = platform.create_user("dr_smith", "smith@school.edu", UserRole.TEACHER)
    
    # Simulate different levels of progress for each student
    ai_basics_id = list(platform.modules.keys())[0]
    ethics_id = list(platform.modules.keys())[1]
    
    # Emma - High performer (100% on AI Basics)
    platform.update_progress(students[0].id, ai_basics_id, 100.0, 45)
    if students[0].id in platform.user_progress and ai_basics_id in platform.user_progress[students[0].id]:
        platform.user_progress[students[0].id][ai_basics_id].quiz_scores = [88, 92, 85, 90]
    
    # James - Average performer (70% on AI Basics)
    platform.update_progress(students[1].id, ai_basics_id, 70.0, 60)
    if students[1].id in platform.user_progress and ai_basics_id in platform.user_progress[students[1].id]:
        platform.user_progress[students[1].id][ai_basics_id].quiz_scores = [65, 72, 68]
    
    # Maria - Struggling (40% on AI Basics)
    platform.update_progress(students[2].id, ai_basics_id, 40.0, 80)
    if students[2].id in platform.user_progress and ai_basics_id in platform.user_progress[students[2].id]:
        platform.user_progress[students[2].id][ai_basics_id].quiz_scores = [45, 52, 48]
    
    print("\n📚 SAMPLE MODULE STRUCTURE:")
    for module_id, module in platform.modules.items():
        print(f"\n🎯 {module.title}")
        print(f"   Category: {module.category.value.replace('_', ' ').title()}")
        print(f"   Difficulty: {module.difficulty.value.title()}")
        print(f"   Duration: {module.estimated_duration} minutes")
        print(f"   Content Blocks: {len(module.content_blocks)}")
        print(f"   Assessment Questions: {len(module.assessment_questions)}")
        if module.prerequisites:
            print(f"   Prerequisites: {len(module.prerequisites)} required")
    
    print("\n👥 STUDENT PROGRESS EXAMPLES:")
    for student in students:
        print(f"\n📊 {student.username.replace('_', ' ').title()}:")
        learning_path = platform.get_personalized_learning_path(student.id)
        print(f"   Available Modules: {len(learning_path)}")
        
        for module_id, progress in student.progress.items():
            module_name = platform.modules[module_id].title
            print(f"   • {module_name}: {progress:.1f}% complete")
        
        # Show adaptive feedback for each student
        if student.progress:
            module_id = list(student.progress.keys())[0]
            feedback = platform.get_adaptive_feedback(student.id, module_id, {"quiz_score": 75})
            print(f"   💡 Feedback: {feedback['message']}")
            if feedback['suggestions']:
                print(f"   📝 Suggestions: {', '.join(feedback['suggestions'][:2])}")
    
    print("\n🎲 SAMPLE SCENARIO OUTPUT:")
    scenario = list(platform.scenarios.values())[0]
    print(f"\n📋 Scenario: {scenario.title}")
    print(f"📝 Context: {scenario.context}")
    print(f"🎯 Challenge: {scenario.challenge}")
    print("\n💭 Decision Options:")
    for i, option in enumerate(scenario.options, 1):
        print(f"   {i}. {option['text']}")
        print(f"      → Consequence: {option['consequence']}")
        print(f"      → Ethics Score: {option['ethics_score']}/10")
    
    print("\n🔍 ETHICAL CONSIDERATIONS:")
    for consideration in scenario.ethical_considerations:
        print(f"   • {consideration}")
    
    print("\n🎓 LEARNING OBJECTIVES:")
    for objective in scenario.learning_objectives:
        print(f"   • {objective}")
    
    print("\n📈 TEACHER DASHBOARD SAMPLE:")
    dashboard = platform.get_teacher_dashboard_data(teacher.id)
    print(f"👨‍🏫 Teacher: {teacher.username.replace('_', ' ').title()}")
    print(f"📊 Class Overview:")
    print(f"   Total Students: {dashboard['total_students']}")
    print(f"   Module Completion Rates:")
    for module, rate in dashboard['module_completion_rates'].items():
        print(f"   • {module}: {rate:.1f}%")
    
    print(f"\n👥 Individual Student Progress:")
    for student_data in dashboard['student_progress']:
        print(f"   📚 {student_data['student_name'].replace('_', ' ').title()}:")
        print(f"      Overall Completion: {student_data['completion_rate']:.1f}%")
        print(f"      Time Spent: {student_data['time_spent']} minutes")
        print(f"      Last Active: {student_data['last_active'].strftime('%Y-%m-%d %H:%M')}")
    
    print("\n🎯 ASSESSMENT QUESTION EXAMPLE:")
    module = list(platform.modules.values())[0]
    if module.assessment_questions:
        question = module.assessment_questions[0]
        print(f"❓ {question['question']}")
        for i, option in enumerate(question['options'], 1):
            marker = "✓" if i-1 == question['correct'] else " "
            print(f"   {marker} {i}. {option}")
        print(f"💡 Explanation: {question['explanation']}")
    
    print("\n🚀 PERSONALIZED LEARNING PATH EXAMPLE:")
    student = students[0]  # Emma - high performer
    path = platform.get_personalized_learning_path(student.id)
    print(f"📚 Recommended path for {student.username.replace('_', ' ').title()}:")
    for i, module in enumerate(path, 1):
        prerequisites = f" (requires {len(module.prerequisites)} prerequisites)" if module.prerequisites else ""
        print(f"   {i}. {module.title} - {module.difficulty.value.title()}{prerequisites}")
    
    print("\n" + "="*60)
    print("END OF PLATFORM DEMONSTRATION")
    print("="*60)