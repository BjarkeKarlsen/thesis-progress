// This file runs in the BROWSER, NOT on the server
// It uses the DOM to display flashcards
// Math is ALREADY rendered server-side - just display it!

let flashcardData = {};
let currentSubject = null;
let currentCardIndex = 0;
let flipped = false;
let masteredCards = new Set();

// Fetch flashcard data from API
async function loadFlashcards() {
  try {
    const response = await fetch('/api/flashcards');
    flashcardData = await response.json();
    console.log('✅ Flashcards loaded (with pre-rendered math)');
    initializeApp();
  } catch (error) {
    console.error('Error loading flashcards:', error);
    alert('Failed to load flashcards');
  }
}

function initializeApp() {
  renderSubjectButtons();
  const firstTopicId = flashcardData.topics[0].id;
  loadSubject(firstTopicId);
}

function renderSubjectButtons() {
  const selector = document.getElementById('subjectSelector');
  selector.innerHTML = '';

  flashcardData.topics.forEach((topic, index) => {
    const btn = document.createElement('button');
    btn.className = 'subject-btn';
    if (index === 0) btn.classList.add('active');
    btn.textContent = topic.name;
    btn.addEventListener('click', () => loadSubject(topic.id));
    selector.appendChild(btn);
  });
}

function loadSubject(subjectId) {
  currentSubject = subjectId;
  currentCardIndex = 0;
  flipped = false;
  masteredCards.clear();

  document.querySelectorAll('.subject-btn').forEach((btn, index) => {
    const topicId = flashcardData.topics[index].id;
    btn.classList.toggle('active', topicId === subjectId);
  });

  displayCard();
  updateStats();
}

function displayCard() {
  const topic = flashcardData.topics.find(t => t.id === currentSubject);
  if (!topic) return;

  const cards = topic.cards;
  const card = cards[currentCardIndex];

  const label = flipped ? 'Answer' : 'Question';
  const text = flipped ? card.a : card.q;

  document.getElementById('cardLabel').textContent = label;
  document.getElementById('cardCounter').textContent = `Card ${currentCardIndex + 1} of ${cards.length}`;

  const progress = ((currentCardIndex + 1) / cards.length) * 100;
  document.getElementById('progressFill').style.width = progress + '%';

  document.getElementById('prevBtn').disabled = currentCardIndex === 0;
  document.getElementById('nextBtn').disabled = currentCardIndex === cards.length - 1;

  updateFlashcardStyle();

  // ✅ SIMPLE - Just display the pre-rendered HTML from server
  // text is ALREADY beautiful math HTML from server - no rendering needed!
  const cardTextElement = document.getElementById('cardText');
  cardTextElement.innerHTML = text;
}

function updateFlashcardStyle() {
  const flashcard = document.getElementById('flashcard');
  if (flipped) {
    flashcard.style.background = 'linear-gradient(135deg, #4caf50 0%, #3d8b40 100%)';
  } else {
    flashcard.style.background = 'linear-gradient(135deg, #2186B4 0%, #1a6a94 100%)';
  }
}

function flipCard() {
  flipped = !flipped;
  displayCard();
}

function previousCard() {
  if (currentCardIndex > 0) {
    currentCardIndex--;
    flipped = false;
    displayCard();
  }
}

function nextCard() {
  const topic = flashcardData.topics.find(t => t.id === currentSubject);
  if (currentCardIndex < topic.cards.length - 1) {
    currentCardIndex++;
    flipped = false;
    displayCard();
  }
}

function markAsKnown() {
  masteredCards.add(currentCardIndex);
  updateStats();
  nextCard();
}

function updateStats() {
  const topic = flashcardData.topics.find(t => t.id === currentSubject);
  const cards = topic.cards;
  const mastered = masteredCards.size;
  const remaining = cards.length - mastered;
  const accuracy = cards.length > 0 ? Math.round((mastered / cards.length) * 100) : 0;

  document.getElementById('masteredCount').textContent = mastered;
  document.getElementById('remainingCount').textContent = remaining;
  document.getElementById('accuracyPercent').textContent = accuracy + '%';
}

// Only attach event listeners if we're in the browser
if (typeof document !== 'undefined') {
  document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ DOMContentLoaded fired');
    
    // Event listeners
    document.getElementById('flashcard').addEventListener('click', flipCard);
    document.getElementById('prevBtn').addEventListener('click', previousCard);
    document.getElementById('nextBtn').addEventListener('click', nextCard);
    document.getElementById('knowBtn').addEventListener('click', markAsKnown);

    // Load flashcards when page loads
    loadFlashcards();
  });
}